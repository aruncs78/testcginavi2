from pathlib import Path
import sys
from playwright.sync_api import expect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from login_page import LoginPage
from inventory_page import InventoryPage
from cart_page import CartPage
from checkout_page import CheckoutPage
from config import STANDARD_USER, PASSWORD, CHECKOUT_INFO


BACKPACK = 'sauce-labs-backpack'
BIKE_LIGHT = 'sauce-labs-bike-light'
FLEECE = 'sauce-labs-fleece-jacket'


def login_and_open_cart(page, items=None):
    LoginPage(page).login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(page)
    inventory.assert_loaded()
    for item in items or []:
        inventory.add_item(item)
    inventory.open_cart()
    return CartPage(page)


def test_cart_shows_selected_item_and_continue_shopping(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK])
    cart.assert_item_present('Sauce Labs Backpack')
    cart.continue_shopping()
    expect(app_page.locator('[data-test="title"]')).to_have_text('Products')


def test_remove_item_from_cart(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK, BIKE_LIGHT])
    cart.remove_item(BIKE_LIGHT)
    expect(app_page.locator('[data-test="inventory-item"]')).to_have_count(1)


def test_checkout_information_required_validations(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK])
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.continue_checkout()
    checkout.assert_error('First Name is required')
    checkout.fill_information(first_name='Arun')
    checkout.continue_checkout()
    checkout.assert_error('Last Name is required')
    checkout.fill_information(first_name='Arun', last_name='Sane')
    checkout.continue_checkout()
    checkout.assert_error('Postal Code is required')


def test_cancel_checkout_from_information_step(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK])
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.cancel()
    expect(app_page).to_have_url('https://www.saucedemo.com/cart.html')


def test_checkout_overview_and_finish_single_item_order(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK])
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.fill_information(**CHECKOUT_INFO)
    checkout.continue_checkout()
    expect(app_page.locator('[data-test="inventory-item-name"]')).to_have_text(['Sauce Labs Backpack'])
    expect(app_page.locator('[data-test="subtotal-label"]')).to_contain_text('$29.99')
    checkout.finish()
    checkout.assert_complete()
    checkout.back_home_button.click()
    expect(app_page.locator('[data-test="title"]')).to_have_text('Products')


def test_checkout_multiple_items_end_to_end(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK, BIKE_LIGHT, FLEECE])
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.fill_information(**CHECKOUT_INFO)
    checkout.continue_checkout()
    expect(app_page.locator('[data-test="inventory-item"]')).to_have_count(3)
    checkout.finish()
    checkout.assert_complete()


def test_add_item_from_detail_page_then_complete_purchase(app_page):
    LoginPage(app_page).login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(app_page)
    inventory.assert_loaded()
    app_page.locator('[data-test="item-4-title-link"]').click()
    app_page.locator('[data-test="add-to-cart"]').click()
    inventory.open_cart()
    cart = CartPage(app_page)
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.fill_information(**CHECKOUT_INFO)
    checkout.continue_checkout()
    checkout.finish()
    checkout.assert_complete()


def test_remove_item_before_checkout_updates_order_contents(app_page):
    cart = login_and_open_cart(app_page, [BACKPACK, BIKE_LIGHT])
    cart.remove_item(BIKE_LIGHT)
    cart.checkout()
    checkout = CheckoutPage(app_page)
    checkout.fill_information(**CHECKOUT_INFO)
    checkout.continue_checkout()
    expect(app_page.locator('[data-test="inventory-item"]')).to_have_count(1)
    expect(app_page.locator('[data-test="inventory-item-name"]')).to_have_text(['Sauce Labs Backpack'])
