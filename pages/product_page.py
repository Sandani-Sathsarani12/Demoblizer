from playwright.sync_api import Page

from pages.base_page import BasePage


class ProductPage(BasePage):
    TITLE = ".name"
    PRICE = ".price-container"
    DESCRIPTION = "#more-information"
    IMAGE = ".product-image img"
    ADD_TO_CART = "a[onclick*=addToCart]"

    def add_to_cart(self) -> None:
        self.click(self.ADD_TO_CART)

    def details(self) -> dict[str, str | bool]:
        return {
            "title": self.text(self.TITLE),
            "price": self.text(self.PRICE),
            "description": self.text(self.DESCRIPTION),
            "image": self.page.locator(self.IMAGE).is_visible(),
        }
