from playwright.sync_api import Page

from pages.base_page import BasePage


class HomePage(BasePage):
    PRODUCTS = ".card-title a"
    PRODUCT_CARDS = ".card"
    CATEGORY_LINK = "#cat"
    PHONE_CATEGORY = "a[onclick*=phone]"
    LAPTOP_CATEGORY = "a[onclick*=notebook]"
    MONITOR_CATEGORY = "a[onclick*=monitor]"
    NEXT = "#next2"
    PREVIOUS = "#prev2"
    LOGIN = "#login2"
    SIGNUP = "#signin2"
    CART = "#cartur"
    LOGOUT = "#logout2"
    WELCOME = "#nameofuser"

    def load(self) -> None:
        self.navigate("/")
        self.page.locator(self.PRODUCTS).first.wait_for(state="visible")

    def product_names(self) -> list[str]:
        return self.page.locator(self.PRODUCTS).all_inner_texts()

    def open_product(self, name: str) -> None:
        self.page.get_by_role("link", name=name, exact=True).click()

    def select_category(self, category: str) -> None:
        locator = {"phones": self.PHONE_CATEGORY, "laptops": self.LAPTOP_CATEGORY, "monitors": self.MONITOR_CATEGORY}[category]
        self.click(locator)

    def open_login(self) -> None:
        self.click(self.LOGIN)

    def open_signup(self) -> None:
        self.click(self.SIGNUP)

    def open_cart(self) -> None:
        self.click(self.CART)
