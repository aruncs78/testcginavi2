# SauceDemo Playwright Automation Suite

Core functional Playwright test suite for https://www.saucedemo.com using Python, pytest, and Playwright.

## Coverage
- Login validation and successful authentication
- Inventory sorting, add/remove cart actions, and product detail navigation
- Cart behavior and badge validation
- Checkout validation and successful completion flows
- End-to-end purchase flows for single/multiple items

## Run locally
```bash
pip install -r requirements.txt
python -m playwright install chromium
pytest --browser chromium
```

## Reports
The suite is configured to generate:
- pytest-html report
- screenshots on failure
- videos for each test
- traces for each test

## GitHub Actions
Manual workflow available under Actions: `SauceDemo Playwright Tests`.
