import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


def as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://www.demoblaze.com").rstrip("/")
    browser: str = os.getenv("BROWSER", "chromium").lower()
    headless: bool = as_bool(os.getenv("HEADLESS"), True)
    timeout: int = int(os.getenv("TIMEOUT", "15000"))
    retries: int = int(os.getenv("RETRIES", "0"))
    known_bug_policy: str = os.getenv("KNOWN_BUG_POLICY", "report").lower()
    video: bool = as_bool(os.getenv("VIDEO"), False)


settings = Settings()
