from enum import StrEnum

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class FailureCategory(StrEnum):
    APPLICATION_BUG = "APPLICATION_BUG"
    LOCATOR_ISSUE = "LOCATOR_ISSUE"
    ASSERTION_FAILURE = "ASSERTION_FAILURE"
    TEST_DATA_FAILURE = "TEST_DATA_FAILURE"
    TIMEOUT = "TIMEOUT"
    NETWORK_FAILURE = "NETWORK_FAILURE"
    BROWSER_FAILURE = "BROWSER_FAILURE"
    ENVIRONMENT_FAILURE = "ENVIRONMENT_FAILURE"
    UNKNOWN = "UNKNOWN"


def classify_failure(error: BaseException, page=None) -> tuple[FailureCategory, str]:
    message = str(error)
    lowered = message.lower()
    if isinstance(error, PlaywrightTimeoutError):
        if any(term in lowered for term in ("net::", "navigation", "network")):
            return FailureCategory.NETWORK_FAILURE, message
        return FailureCategory.TIMEOUT, message
    if isinstance(error, AssertionError):
        return FailureCategory.ASSERTION_FAILURE, message
    if "strict mode violation" in lowered or "locator(" in lowered or "element is not attached" in lowered:
        return FailureCategory.LOCATOR_ISSUE, message
    if isinstance(error, PlaywrightError):
        if any(term in lowered for term in ("browser", "target page", "context or browser has been closed")):
            return FailureCategory.BROWSER_FAILURE, message
        if "net::" in lowered:
            return FailureCategory.NETWORK_FAILURE, message
        return FailureCategory.ENVIRONMENT_FAILURE, message
    return FailureCategory.UNKNOWN, message
