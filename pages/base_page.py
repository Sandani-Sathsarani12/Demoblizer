from pathlib import Path

from playwright.sync_api import Page

from utils.config import settings
from utils.logger import get_logger


class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger()

    def navigate(self, path: str = "") -> None:
        self.page.goto(f"{settings.base_url}{path}", wait_until="domcontentloaded")

    def click(self, selector: str) -> None:
        self.logger.info("Clicking %s", selector)
        self.page.locator(selector).click(timeout=settings.timeout)

    def fill(self, selector: str, value: str) -> None:
        self.logger.info("Filling %s", selector)
        self.page.locator(selector).fill(value, timeout=settings.timeout)

    def text(self, selector: str) -> str:
        return self.page.locator(selector).inner_text(timeout=settings.timeout)

    def visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible(timeout=settings.timeout)

    def screenshot(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=str(path), full_page=True)
