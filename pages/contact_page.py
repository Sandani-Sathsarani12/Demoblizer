from playwright.sync_api import Page

from pages.base_page import BasePage


class ContactPage(BasePage):
    CONTACT = "#contact-link"
    EMAIL = "#recipient-email"
    NAME = "#recipient-name"
    MESSAGE = "#message-text"
    SUBMIT = "#exampleModal button:has-text('Send message')"

    def open(self) -> None:
        self.open_home()
        self.click(self.CONTACT)
        self.page.locator("#exampleModal").wait_for(state="visible")

    def open_home(self) -> None:
        self.navigate("/")

    def fill_form(self, email: str, name: str, message: str) -> None:
        self.fill(self.EMAIL, email)
        self.fill(self.NAME, name)
        self.fill(self.MESSAGE, message)

    def submit(self) -> None:
        self.click(self.SUBMIT)
