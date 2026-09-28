from playwright.sync_api import Page

from pages.base_page import BasePage


class PurchasePage(BasePage):
    PLACE_ORDER = "button:has-text('Place Order')"
    NAME = "#name"
    COUNTRY = "#country"
    CITY = "#city"
    CARD = "#card"
    MONTH = "#month"
    YEAR = "#year"
    SUBMIT = "#orderModal button:has-text('Purchase')"
    CONFIRMATION = ".sweet-alert"

    def open_dialog(self) -> None:
        self.click(self.PLACE_ORDER)
        self.page.locator("#orderModal").wait_for(state="visible")

    def fill_order(self, name: str, country: str, city: str, card: str, month: str, year: str) -> None:
        for selector, value in ((self.NAME, name), (self.COUNTRY, country), (self.CITY, city), (self.CARD, card), (self.MONTH, month), (self.YEAR, year)):
            self.fill(selector, value)

    def purchase(self) -> None:
        self.click(self.SUBMIT)

    def confirmation_text(self) -> str:
        return self.text(self.CONFIRMATION)
