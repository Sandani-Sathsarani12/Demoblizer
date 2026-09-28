# Demoblizer UI Automation

Playwright + Python + Pytest automation for `https://www.demoblaze.com/`, built from `DEMOBLAZE_MASTER_TEST_SUITE.xlsx`. The application is treated as the system under test; known defects remain visible as failures with evidence.

## Stack and structure

- Python 3.11+
- Playwright for Python
- Pytest, pytest-html, and optional Allure
- Page objects in `pages/`
- Excel-derived metadata and users in `data/`
- Configuration, logging, evidence, and failure classification in `utils/`
- Candidate tests in `tests/test_excel_coverage.py`
- CI in `.github/workflows/playwright-tests.yml`

The source workbook contains 102 cases. 71 are marked `Yes` for automation, 30 are marked `No`, and TC028 is explicitly marked `No (multi-step transactional flow)`. The 71 candidate IDs are preserved in test method names and traceability documentation.

## Install on Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
playwright install
Copy-Item .env.example .env
```

PowerShell configuration example:

```powershell
$env:HEADLESS = "false"
$env:BROWSER = "chromium"
```

Command Prompt equivalent:

```bat
set HEADLESS=false && pytest -v
```

## Run tests

```powershell
pytest -v
pytest -m smoke -v
pytest -m regression -v
pytest -m security -v
pytest tests/test_excel_coverage.py -k TC001 -v
pytest tests/test_excel_coverage.py -v --html=reports/report.html --self-contained-html --alluredir=reports/allure-results
```

Supported browsers are `chromium`, `firefox`, and `webkit`. Set `BROWSER`, `BASE_URL`, `TIMEOUT`, `VIDEO`, and `KNOWN_BUG_POLICY` in `.env` or the shell. Defaults are Chromium, headless mode, 15 seconds, no video, and `report` for known bugs.

## Evidence and failure classification

Failures create `screenshots/TC###_failure.png`, Playwright traces in `traces/TC###.zip`, and structured logs in `reports/logs/test-run.log`. The classifier distinguishes `APPLICATION_BUG`, `LOCATOR_ISSUE`, `ASSERTION_FAILURE`, `TEST_DATA_FAILURE`, `TIMEOUT`, `NETWORK_FAILURE`, `BROWSER_FAILURE`, `ENVIRONMENT_FAILURE`, and `UNKNOWN` using exception type and evidence. The original exception is preserved.

Tests linked to an open bug use markers such as `bug_001`. With `KNOWN_BUG_POLICY=report`, a matching failure is reported as a known application defect but is not silently converted to pass. `fail` keeps the failure blocking; `allow` is available for teams that explicitly choose non-blocking known defects.

## Reports and artifacts

- HTML: `reports/report.html`
- Allure raw results: `reports/allure-results/`
- View Allure after installing the Allure CLI: `allure serve reports/allure-results`
- Screenshots, traces, videos, and logs are retained locally and uploaded by GitHub Actions.

## CI/CD

The workflow runs on pushes to `main`, pull requests, and manual dispatch. It supports a browser matrix and uploads reports and evidence even when tests fail. GitHub Actions uses its built-in `GITHUB_TOKEN` only for workflow operations; no personal token is required in source files.

## Source traceability

See [docs/AUTOMATION_COVERAGE.md](docs/AUTOMATION_COVERAGE.md) and [docs/TEST_CASE_TRACEABILITY.md](docs/TEST_CASE_TRACEABILITY.md). The original workbook remains outside the repository root unless deliberately copied in; no credentials from the workbook are committed.

## Troubleshooting

- Run `playwright install` if browser launch fails.
- Use `HEADLESS=false` to inspect a local failure.
- Check `reports/logs/test-run.log` and the matching trace before changing a locator.
- Set `KNOWN_BUG_POLICY=fail` when known defects must block CI.
- Authenticate GitHub securely with `gh auth login` or Git Credential Manager. Never paste a token into source, YAML, or chat.
