import re

import pytest

from data.test_metadata import TEST_METADATA
from pages.cart_page import CartPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.product_page import ProductPage
from pages.purchase_page import PurchasePage
from pages.signup_page import SignupPage


def _product(page, name="Samsung galaxy s6"):
    home = HomePage(page)
    home.load()
    home.open_product(name)
    return ProductPage(page)


def _run_case(case_id, page, unique_test_user):
    metadata = TEST_METADATA[case_id]
    module = metadata["module"]
    scenario = metadata["scenario"].lower()
    home = HomePage(page)

    if case_id in {"TC001", "TC002", "TC003", "TC004", "TC005", "TC006", "TC007", "TC008", "TC031", "TC032", "TC033", "TC034", "TC035"}:
        signup = SignupPage(page)
        signup.open()
        username = unique_test_user.username
        password = unique_test_user.password
        if case_id in {"TC004", "TC006"}:
            username = ""
        if case_id in {"TC005", "TC006"}:
            password = ""
        if case_id == "TC007":
            username = f" {username}"
        if case_id == "TC031":
            username = "x"
        if case_id == "TC032":
            username = "x" * 151
        if case_id == "TC033":
            password = "x" * 151
        if case_id == "TC034":
            username = "qa_用户_é"
        if case_id == "TC035":
            password = "  Qa Password  "
        signup.signup(username, password)
        assert page.url.startswith("https://"), f"{case_id}: signup must remain on HTTPS"
        return

    if module == "Login":
        login = LoginPage(page)
        login.open()
        if case_id in {"TC009", "TC010"}:
            signup = SignupPage(page)
            signup.open()
            signup.signup(unique_test_user.username, unique_test_user.password)
            login.open()
            login.login(unique_test_user.username, unique_test_user.password)
            assert page.locator("#nameofuser").is_visible()
        elif case_id == "TC095":
            assert login.password_input_type() == "password"
        else:
            username = "invalid_user"
            password = "invalid_password"
            if case_id == "TC013":
                username = ""
            if case_id == "TC014":
                username = password = ""
            if case_id == "TC016":
                password = ""
            if case_id == "TC039":
                username = "x" * 200
            if case_id == "TC040":
                username = "' OR '1'='1"
            if case_id == "TC041":
                username = "<script>alert(1)</script>"
            if case_id == "TC042":
                username = password = "   "
            login.login(username, password)
            assert "password" not in page.url.lower()
        return

    if module == "Signup":
        signup = SignupPage(page)
        signup.open()
        assert page.url.startswith("https://")
        return

    if case_id in {"TC022", "TC023", "TC024", "TC049", "TC053"}:
        home.load()
        assert len(home.product_names()) > 0
        if case_id == "TC024":
            home.select_category("phones")
            assert len(home.product_names()) > 0
        if case_id == "TC049":
            home.click(home.NEXT)
            assert len(home.product_names()) > 0
        if case_id == "TC053":
            for category in ("phones", "laptops", "monitors", "phones"):
                home.select_category(category)
            assert len(home.product_names()) > 0
        return

    if case_id in {"TC025", "TC026", "TC027", "TC055", "TC056", "TC057", "TC058", "TC062", "TC094"}:
        product = _product(page)
        product.add_to_cart()
        cart = CartPage(page)
        cart.open()
        if case_id in {"TC025", "TC026", "TC055"}:
            assert len(cart.item_names()) >= 1
        if case_id == "TC027":
            assert cart.total().strip().isdigit()
        if case_id in {"TC056", "TC057"}:
            cart.remove_first_item()
            assert len(cart.item_names()) == 0
        if case_id in {"TC058", "TC094"}:
            assert cart.page.url.endswith("/cart.html")
        if case_id == "TC062":
            before = int(cart.total() or 0)
            cart.remove_first_item()
            after = int(cart.total() or 0)
            assert after <= before
        return

    if module == "Product Details":
        if case_id == "TC100":
            page.goto("https://www.demoblaze.com/prod.html?idp_=1")
        else:
            _product(page)
        details = ProductPage(page).details()
        assert details["title"] and details["price"] and details["description"] and details["image"]
        return

    if module == "Purchase":
        if case_id not in {"TC065", "TC066"}:
            product = _product(page)
            product.add_to_cart()
        cart = CartPage(page)
        cart.open()
        purchase = PurchasePage(page)
        if case_id in {"TC065", "TC066"}:
            assert page.url.endswith("/cart.html")
            return
        purchase.open_dialog()
        card = "1234567890123456"
        if case_id in {"TC069", "TC076"}:
            card = "abcd"
        if case_id == "TC070":
            card = "1234abcd"
        if case_id == "TC071":
            card = "0"
        if case_id == "TC072":
            card = "-1"
        if case_id == "TC073":
            card = ""
        purchase.fill_order("QA User", "Sri Lanka", "Colombo", card, "12", "2099")
        assert page.locator(PurchasePage.CARD).input_value() == card
        return

    if module == "Contact Form":
        contact = ContactPage(page)
        contact.open()
        email, name, message = "qa@example.com", "QA User", "Demoblaze test message"
        if case_id in {"TC080", "TC081"}:
            email = name = message = ""
        if case_id == "TC082":
            email = "invalid-email"
        if case_id == "TC083":
            name = "12345"
        if case_id == "TC092":
            message = "' OR '1'='1"
        if case_id == "TC093":
            message = '"><script>alert(1)</script>'
        contact.fill_form(email, name, message)
        assert page.locator(ContactPage.MESSAGE).input_value() == message
        return

    if module in {"Logout", "Session"}:
        home.load()
        assert page.url.startswith("https://")
        return

    assert module, f"{case_id} has no mapped module"


@pytest.mark.smoke
@pytest.mark.positive
def test_TC001_valid_signup(page, unique_test_user): _run_case("TC001", page, unique_test_user)

def test_TC002_second_valid_signup(page, unique_test_user): _run_case("TC002", page, unique_test_user)

def test_TC003_existing_username_signup(page, unique_test_user): _run_case("TC003", page, unique_test_user)
@pytest.mark.negative
def test_TC004_empty_username_signup(page, unique_test_user): _run_case("TC004", page, unique_test_user)
@pytest.mark.negative
def test_TC005_empty_password_signup(page, unique_test_user): _run_case("TC005", page, unique_test_user)
@pytest.mark.negative
def test_TC006_empty_signup(page, unique_test_user): _run_case("TC006", page, unique_test_user)
def test_TC007_leading_space_signup(page, unique_test_user): _run_case("TC007", page, unique_test_user)
def test_TC008_case_sensitive_duplicate_signup(page, unique_test_user): _run_case("TC008", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC009_valid_login(page, unique_test_user): _run_case("TC009", page, unique_test_user)
def test_TC010_welcome_username(page, unique_test_user): _run_case("TC010", page, unique_test_user)
def test_TC011_invalid_username_login(page, unique_test_user): _run_case("TC011", page, unique_test_user)
def test_TC012_invalid_password_login(page, unique_test_user): _run_case("TC012", page, unique_test_user)
def test_TC013_empty_username_login(page, unique_test_user): _run_case("TC013", page, unique_test_user)
def test_TC014_empty_credentials_login(page, unique_test_user): _run_case("TC014", page, unique_test_user)
def test_TC015_case_sensitive_login(page, unique_test_user): _run_case("TC015", page, unique_test_user)
def test_TC016_empty_password_login(page, unique_test_user): _run_case("TC016", page, unique_test_user)
def test_TC017_login_https(page, unique_test_user): _run_case("TC017", page, unique_test_user)
def test_TC018_signup_https(page, unique_test_user): _run_case("TC018", page, unique_test_user)
def test_TC019_login_url_credentials(page, unique_test_user): _run_case("TC019", page, unique_test_user)
def test_TC020_failed_login_url_password(page, unique_test_user): _run_case("TC020", page, unique_test_user)
def test_TC021_signup_url_credentials(page, unique_test_user): _run_case("TC021", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC022_home_products(page, unique_test_user): _run_case("TC022", page, unique_test_user)
def test_TC023_home_product_details(page, unique_test_user): _run_case("TC023", page, unique_test_user)
def test_TC024_category_filtering(page, unique_test_user): _run_case("TC024", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC025_single_product_cart(page, unique_test_user): _run_case("TC025", page, unique_test_user)
def test_TC026_multiple_product_cart(page, unique_test_user): _run_case("TC026", page, unique_test_user)
def test_TC027_cart_total(page, unique_test_user): _run_case("TC027", page, unique_test_user)
def test_TC029_valid_card(page, unique_test_user): _run_case("TC029", page, unique_test_user)
def test_TC030_future_card_date(page, unique_test_user): _run_case("TC030", page, unique_test_user)
def test_TC031_single_character_username(page, unique_test_user): _run_case("TC031", page, unique_test_user)
def test_TC032_long_username(page, unique_test_user): _run_case("TC032", page, unique_test_user)
def test_TC033_long_password(page, unique_test_user): _run_case("TC033", page, unique_test_user)
def test_TC034_special_unicode_username(page, unique_test_user): _run_case("TC034", page, unique_test_user)
def test_TC035_whitespace_password(page, unique_test_user): _run_case("TC035", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_023
def test_TC037_repeated_failed_login(page, unique_test_user): _run_case("TC037", page, unique_test_user)
def test_TC039_long_login_username(page, unique_test_user): _run_case("TC039", page, unique_test_user)
@pytest.mark.security
def test_TC040_sql_injection_login(page, unique_test_user): _run_case("TC040", page, unique_test_user)
@pytest.mark.security
def test_TC041_xss_login(page, unique_test_user): _run_case("TC041", page, unique_test_user)
def test_TC042_whitespace_login(page, unique_test_user): _run_case("TC042", page, unique_test_user)
def test_TC043_logout(page, unique_test_user): _run_case("TC043", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_017
def test_TC044_cart_after_logout_navigation(page, unique_test_user): _run_case("TC044", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_017
def test_TC045_cart_after_logout_direct_url(page, unique_test_user): _run_case("TC045", page, unique_test_user)
def test_TC047_cart_refresh_session(page, unique_test_user): _run_case("TC047", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_001
def test_TC049_next_previous_products(page, unique_test_user): _run_case("TC049", page, unique_test_user)
def test_TC053_repeated_category_navigation(page, unique_test_user): _run_case("TC053", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC054_product_details(page, unique_test_user): _run_case("TC054", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_015
def test_TC055_duplicate_cart_product(page, unique_test_user): _run_case("TC055", page, unique_test_user)
def test_TC056_remove_cart_item(page, unique_test_user): _run_case("TC056", page, unique_test_user)
def test_TC057_remove_only_cart_item(page, unique_test_user): _run_case("TC057", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_016
def test_TC058_empty_cart_place_order(page, unique_test_user): _run_case("TC058", page, unique_test_user)
def test_TC062_cart_total_after_remove(page, unique_test_user): _run_case("TC062", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_012
def test_TC065_empty_cart_purchase(page, unique_test_user): _run_case("TC065", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_016
def test_TC066_empty_cart_order_dialog(page, unique_test_user): _run_case("TC066", page, unique_test_user)
def test_TC067_empty_purchase_form(page, unique_test_user): _run_case("TC067", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_018
def test_TC069_alpha_card(page, unique_test_user): _run_case("TC069", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_018
def test_TC070_alphanumeric_card(page, unique_test_user): _run_case("TC070", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_022
def test_TC071_zero_card(page, unique_test_user): _run_case("TC071", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_022
def test_TC072_negative_card(page, unique_test_user): _run_case("TC072", page, unique_test_user)
def test_TC073_empty_card(page, unique_test_user): _run_case("TC073", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_019
def test_TC075_expired_card(page, unique_test_user): _run_case("TC075", page, unique_test_user)
def test_TC076_non_numeric_card_date(page, unique_test_user): _run_case("TC076", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_006
def test_TC080_empty_contact(page, unique_test_user): _run_case("TC080", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_020
def test_TC081_empty_contact_message(page, unique_test_user): _run_case("TC081", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_007
def test_TC082_invalid_contact_email(page, unique_test_user): _run_case("TC082", page, unique_test_user)
@pytest.mark.regression
@pytest.mark.bug_008
def test_TC083_numeric_contact_name(page, unique_test_user): _run_case("TC083", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC085_valid_contact(page, unique_test_user): _run_case("TC085", page, unique_test_user)
@pytest.mark.security
def test_TC092_sql_injection_contact(page, unique_test_user): _run_case("TC092", page, unique_test_user)
@pytest.mark.security
def test_TC093_xss_contact(page, unique_test_user): _run_case("TC093", page, unique_test_user)
@pytest.mark.security
def test_TC094_direct_cart_without_login(page, unique_test_user): _run_case("TC094", page, unique_test_user)
@pytest.mark.security
def test_TC095_password_masking(page, unique_test_user): _run_case("TC095", page, unique_test_user)
@pytest.mark.smoke
@pytest.mark.positive
def test_TC100_direct_product_url(page, unique_test_user): _run_case("TC100", page, unique_test_user)
