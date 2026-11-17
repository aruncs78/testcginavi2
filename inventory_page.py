from playwright.sync_api import Page, expect


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.sort_dropdown = page.locator('[data-test="product-sort-container"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.menu_button = page.locator('#react-burger-menu-btn')
        self.logout_link = page.locator('[data-test="logout-sidebar-link"]')

    def assert_loaded(self) -> None:
        expect(self.title).to_have_text('Products')
        expect(self.page.locator('[data-test="inventory-item"]')).to_have_count(6)

    def add_item(self, slug: str) -> None:
        self.page.locator(f'[data-test="add-to-cart-{slug}"]').click()

    def remove_item(self, slug: str) -> None:
        self.page.locator(f'[data-test="remove-{slug}"]').click()

    def open_item(self, slug: str) -> None:
        self.page.locator(f'[data-test="item-{slug}-title-link"]').click()

    def sort_by(self, value: str) -> None:
        self.sort_dropdown.select_option(value)

    def open_cart(self) -> None:
        self.cart_link.click()

    def logout(self) -> None:
        self.menu_button.click()
        self.logout_link.click()
