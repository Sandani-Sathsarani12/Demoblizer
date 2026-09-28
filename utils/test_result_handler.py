from pathlib import Path

from utils.config import ROOT
from utils.failure_classifier import FailureCategory, classify_failure
from utils.logger import get_logger


logger = get_logger()


def test_case_id(nodeid: str) -> str:
    for part in nodeid.split("::"):
        if part.startswith("test_TC"):
            return part.split("_", 2)[1]
    return "UNKNOWN"


def classify_and_log(nodeid: str, error: BaseException, page=None) -> tuple[FailureCategory, str]:
    category, reason = classify_failure(error, page)
    logger.error("%s Failure Category: %s", test_case_id(nodeid), category)
    logger.error("%s Reason: %s", test_case_id(nodeid), reason)
    return category, reason


def evidence_paths(case_id: str) -> dict[str, Path]:
    return {
        "screenshot": ROOT / "screenshots" / f"{case_id}_failure.png",
        "trace": ROOT / "traces" / f"{case_id}.zip",
    }
