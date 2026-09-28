from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright
from pytest_html import extras

from data.test_users import TestUser, unique_user
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from utils.config import ROOT, settings
from utils.failure_classifier import FailureCategory
from utils.logger import get_logger
from utils.test_result_handler import classify_and_log, evidence_paths


logger = get_logger()
known_bug_failures = set()
unexpected_failures = set()


def pytest_configure(config):
    (ROOT / "screenshots").mkdir(exist_ok=True)
    (ROOT / "traces").mkdir(exist_ok=True)
    (ROOT / "videos").mkdir(exist_ok=True)
    (ROOT / "reports" / "logs").mkdir(parents=True, exist_ok=True)


def pytest_runtest_logreport(report):
    if report.when == "call" and report.failed:
        if any(keyword.startswith("bug_") for keyword in report.keywords):
            known_bug_failures.add(report.nodeid)
        else:
            unexpected_failures.add(report.nodeid)


def pytest_sessionfinish(session, exitstatus):
    if settings.known_bug_policy in {"report", "allow"} and known_bug_failures and not unexpected_failures:
        session.exitstatus = 0


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance):
    browser_type = getattr(playwright_instance, settings.browser, None)
    if browser_type is None:
        raise ValueError(f"Unsupported BROWSER={settings.browser}; use chromium, firefox, or webkit")
    instance = browser_type.launch(headless=settings.headless)
    yield instance
    instance.close()


@pytest.fixture
def context(browser, request):
    context = browser.new_context(record_video_dir=str(ROOT / "videos") if settings.video else None)
    context.set_default_timeout(settings.timeout)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield context
    report = getattr(request.node, "rep_call", None)
    case_id = request.node.name.split("_", 2)[1] if request.node.name.startswith("test_TC") else request.node.name
    if report and report.failed:
        context.tracing.stop(path=str(ROOT / "traces" / f"{case_id}.zip"))
    else:
        context.tracing.stop()
    context.close()


@pytest.fixture
def page(context):
    page = context.new_page()
    page.on("console", lambda message: logger.info("Console %s: %s", message.type, message.text))
    yield page
    page.close()


@pytest.fixture
def authenticated_user(page) -> TestUser:
    user = unique_user()
    signup = SignupPage(page)
    signup.open()
    signup.signup(user.username, user.password)
    page.wait_for_timeout(500)
    login = LoginPage(page)
    login.open()
    login.login(user.username, user.password)
    page.wait_for_timeout(500)
    return user


@pytest.fixture
def unique_test_user() -> TestUser:
    return unique_user()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        case_id = item.name.split("_", 2)[1] if item.name.startswith("test_TC") else item.name
        if page:
            paths = evidence_paths(case_id)
            page.screenshot(path=str(paths["screenshot"]), full_page=True)
            report.extras = getattr(report, "extras", [])
            report.extras.append(extras.png(str(paths["screenshot"])))
        classify_and_log(item.nodeid, call.excinfo.value if call.excinfo else AssertionError("test failed"), page)
        if item.get_closest_marker("regression") and any(marker.name.startswith("bug_") for marker in item.iter_markers()):
            logger.error("%s KNOWN APPLICATION DEFECT (policy=%s)", case_id, settings.known_bug_policy)
