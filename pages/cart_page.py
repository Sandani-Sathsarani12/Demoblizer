from playwright.sync_api import Page

from pages.base_page import BasePage


class CartPage(BasePage):
    TABLE_ROWS = "#tbodyid tr"
    TOTAL = "#totalp"
    DELETE_LINK = "a:has-text('Delete')"
    PLACE_ORDER = "button:has-text('Place Order')"

    def open(self) -> None:
        self.navigate("/cart.html")

    def item_names(self) -> list[str]:
        return self.page.locator(f"{self.TABLE_ROWS} td:nth-child(2)").all_inner_texts()

    def total(self) -> str:
        return self.text(self.TOTAL)

    def remove_first_item(self) -> None:
        self.page.locator(self.DELETE_LINK).first.click()

    def place_order_visible(self) -> bool:
        return self.page.locator(self.PLACE_ORDER).is_visible()
