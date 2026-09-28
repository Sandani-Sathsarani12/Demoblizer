from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = "#loginusername"
    PASSWORD = "#loginpassword"
    SUBMIT = "#logInModal button:has-text('Log in')"
    MODAL = "#logInModal"

    def open(self) -> None:
        self.open_home()
        self.page.locator("#login2").click()
        self.page.locator(self.MODAL).wait_for(state="visible")

    def open_home(self) -> None:
        self.navigate("/")

    def login(self, username: str, password: str) -> None:
        self.fill(self.USERNAME, username)
        self.fill(self.PASSWORD, password)
        self.click(self.SUBMIT)

    def password_input_type(self) -> str:
        return self.page.locator(self.PASSWORD).get_attribute("type") or ""
