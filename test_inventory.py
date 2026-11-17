from pathlib import Path
import sys
from playwright.sync_api import expect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from login_page import LoginPage
from inventory_page import InventoryPage
from config import STANDARD_USER, PASSWORD


ITEM_SLUG_BACKPACK = 'sauce-labs-backpack'
ITEM_SLUG_BIKE_LIGHT = 'sauce-labs-bike-light'
ITEM_SLUG_FLEECE = 'sauce-labs-fleece-jacket'


def login(page):
    LoginPage(page).login(STANDARD_USER, PASSWORD)
    inventory = InventoryPage(page)
    inventory.assert_loaded()
    return inventory


def test_inventory_loads_with_products(app_page):
    inventory = login(app_page)
    inventory.assert_loaded()


def test_add_and_remove_single_product_from_inventory(app_page):
    inventory = login(app_page)
    inventory.add_item(ITEM_SLUG_BACKPACK)
    expect(inventory.cart_badge).to_have_text('1')
    inventory.remove_item(ITEM_SLUG_BACKPACK)
    expect(inventory.cart_badge).to_have_count(0)


def test_add_multiple_products_to_cart(app_page):
    inventory = login(app_page)
    inventory.add_item(ITEM_SLUG_BACKPACK)
    inventory.add_item(ITEM_SLUG_BIKE_LIGHT)
    inventory.add_item(ITEM_SLUG_FLEECE)
    expect(inventory.cart_badge).to_have_text('3')


def test_open_product_details_and_return_to_inventory(app_page):
    inventory = login(app_page)
    app_page.locator('[data-test="item-4-title-link"]').click()
    expect(app_page.locator('[data-test="inventory-item-name"]')).to_have_text('Sauce Labs Backpack')
    app_page.locator('[data-test="back-to-products"]').click()
    inventory.assert_loaded()


def test_inventory_sorting_options(app_page):
    inventory = login(app_page)
    inventory.sort_by('za')
    expect(app_page.locator('[data-test="inventory-item-name"]').first).to_have_text('Test.allTheThings() T-Shirt (Red)')
    inventory.sort_by('lohi')
    expect(app_page.locator('[data-test="inventory-item-price"]').first).to_have_text('$7.99')
    inventory.sort_by('hilo')
    expect(app_page.locator('[data-test="inventory-item-price"]').first).to_have_text('$49.99')
    inventory.sort_by('az')
    expect(app_page.locator('[data-test="inventory-item-name"]').first).to_have_text('Sauce Labs Backpack')
