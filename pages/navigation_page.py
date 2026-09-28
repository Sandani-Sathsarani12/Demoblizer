from pages.base_page import BasePage


class NavigationPage(BasePage):
    def logout(self) -> None:
        self.click("#logout2")

    def welcome_text(self) -> str:
        return self.text("#nameofuser")

    def cart_link_visible(self) -> bool:
        return self.page.locator("#cartur").is_visible()
