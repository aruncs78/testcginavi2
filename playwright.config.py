from pathlib import Path

BASE_URL = "https://www.saucedemo.com"
ARTIFACTS_DIR = Path("artifacts")
REPORTS_DIR = Path("reports")
ARTIFACTS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
