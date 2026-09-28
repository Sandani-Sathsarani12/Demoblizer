from playwright.sync_api import Page

from pages.base_page import BasePage


class SignupPage(BasePage):
    USERNAME = "#sign-username"
    PASSWORD = "#sign-password"
    SUBMIT = "#signInModal button:has-text('Sign up')"

    def open(self) -> None:
        self.open_home()
        self.page.locator("#signin2").click()
        self.page.locator("#signInModal").wait_for(state="visible")

    def open_home(self) -> None:
        self.navigate("/")

    def signup(self, username: str, password: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def username_value(self) -> str:
        return self.page.locator(self.USERNAME).input_value()
