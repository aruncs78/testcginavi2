from pathlib import Path
import sys
import pytest
from playwright.sync_api import expect

sys.path.insert(0, str(Path(__file__).resolve().parent))
from login_page import LoginPage
from inventory_page import InventoryPage
from config import BASE_URL, STANDARD_USER, LOCKED_OUT_USER, PASSWORD


def test_successful_login(app_page):
    login_page = LoginPage(app_page)
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page = InventoryPage(app_page)
    inventory_page.assert_loaded()


def test_locked_out_user_cannot_login(app_page):
    login_page = LoginPage(app_page)
    login_page.login(LOCKED_OUT_USER, PASSWORD)
    login_page.assert_error('Sorry, this user has been locked out.')


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    [
        ('', PASSWORD, 'Username is required'),
        (STANDARD_USER, '', 'Password is required'),
        ('', '', 'Username is required'),
    ],
)
def test_login_required_field_validation(app_page, username, password, message):
    login_page = LoginPage(app_page)
    login_page.login(username, password)
    login_page.assert_error(message)


def test_logout_from_inventory(app_page):
    login_page = LoginPage(app_page)
    login_page.login(STANDARD_USER, PASSWORD)
    inventory_page = InventoryPage(app_page)
    inventory_page.logout()
    expect(app_page).to_have_url(BASE_URL + '/')
