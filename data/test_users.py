from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class TestUser:
    username: str
    password: str


def unique_user(prefix: str = "qa_user") -> TestUser:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
    return TestUser(f"{prefix}_{stamp}", "QaPassword12!")
