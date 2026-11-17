from playwright.sync_api import Page, expect


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        self.cancel_button = page.locator('[data-test="cancel"]')
        self.finish_button = page.locator('[data-test="finish"]')
        self.error = page.locator('[data-test="error"]')
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')

    def fill_information(self, first_name: str = "", last_name: str = "", postal_code: str = "") -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.postal_code.fill(postal_code)

    def continue_checkout(self) -> None:
        self.continue_button.click()

    def cancel(self) -> None:
        self.cancel_button.click()

    def finish(self) -> None:
        self.finish_button.click()

    def assert_error(self, message: str) -> None:
        expect(self.error).to_contain_text(message)

    def assert_complete(self) -> None:
        expect(self.complete_header).to_have_text('Thank you for your order!')
