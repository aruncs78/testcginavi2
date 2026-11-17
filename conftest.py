from pathlib import Path
import sys
import pytest
from playwright.sync_api import BrowserContext, Page

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import BASE_URL


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "record_video_dir": str(Path("artifacts/videos")),
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture(scope="session", autouse=True)
def ensure_dirs():
    Path("artifacts/screenshots").mkdir(parents=True, exist_ok=True)
    Path("artifacts/videos").mkdir(parents=True, exist_ok=True)
    Path("artifacts/traces").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(parents=True, exist_ok=True)


@pytest.fixture
def app_page(page: Page, context: BrowserContext, request: pytest.FixtureRequest) -> Page:
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page.goto(BASE_URL, wait_until="domcontentloaded")
    yield page
    safe_name = request.node.name.replace("/", "_").replace(" ", "_")
    trace_path = Path("artifacts/traces") / f"{safe_name}.zip"
    context.tracing.stop(path=str(trace_path))


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture(autouse=True)
def capture_failure_artifacts(request: pytest.FixtureRequest, page: Page):
    yield
    rep = getattr(request.node, "rep_call", None)
    if rep and rep.failed:
        file_name = request.node.name.replace("/", "_").replace(" ", "_")
        page.screenshot(path=f"artifacts/screenshots/{file_name}.png", full_page=True)
