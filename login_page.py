from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    def open(self, base_url: str) -> None:
        self.page.goto(base_url, wait_until="domcontentloaded")

    def login(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def assert_error(self, text: str) -> None:
        expect(self.error).to_contain_text(text)
