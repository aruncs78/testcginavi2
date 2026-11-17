from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_items = page.locator('[data-test="inventory-item"]')
        self.checkout_button = page.locator('[data-test="checkout"]')
        self.continue_shopping_button = page.locator('[data-test="continue-shopping"]')

    def assert_item_present(self, item_name: str) -> None:
        expect(self.page.locator('[data-test="inventory-item-name"]')).to_contain_text([item_name])

    def remove_item(self, slug: str) -> None:
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def checkout(self) -> None:
        self.checkout_button.click()

    def continue_shopping(self) -> None:
        self.continue_shopping_button.click()
