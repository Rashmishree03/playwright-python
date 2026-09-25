import pytest
from playwright.sync_api import Playwright, sync_playwright
from src.pages.login_page import LoginPage
from src.utils.config_reader import ConfigReader


"""
Fixture = provides something to your test.
Hook = lets you customize/control Pytest itself.
pytest_addoption is a hook function that allows you to add custom command-line options to pytest. 
In this case, it adds a --browser option that allows the user to specify 
which browser to run tests against (chromium, firefox, or webkit). The default value is set to "chromium".
"""
def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",  # Take the value provided after --browser and store it. Ex: if pytest --browser firefox then browser=firefox
        default="chromium",
        help="Browser to run tests against (chromium, firefox, webkit)"
    )

    parser.addoption(
    "--headed",
    action="store_true",
    default=False,
    help="Run browser in headed mode"
    )

    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against"
    )

@pytest.fixture(scope="session")
def config(request):
    environment = request.config.getoption("--env")
    return ConfigReader(environment)

"""
playwright_instance fixture initializes the Playwright instance and yields it for use in tests.
browser fixture launches the specified browser (chromium, firefox, or webkit) based on the command-line option provided. 
It yields the browser instance for use in tests and ensures that the browser is
    closed after the tests are done.
"""
@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright

"""
two dependencies:
playwright_instance: Playwright - The fixture that initializes the Playwright instance.
request: is a built-in pytest fixture and is used to access the command-line options provided by pytest.
"""
@pytest.fixture(scope="session")
def browser(playwright_instance: Playwright, request):
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    print(f"Running tests on {browser_name} browser")
    print(f"Headed mode: {headed}")

    if browser_name == "chromium":
        browser = playwright_instance.chromium.launch(headless=not headed)

    elif browser_name == "firefox":
        browser = playwright_instance.firefox.launch(headless=not headed)

    elif browser_name == "webkit":
        browser = playwright_instance.webkit.launch(headless=not headed)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    yield browser

    browser.close()

@pytest.fixture
def context(browser, config):
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        base_url=config.get("base_url")
    )
    yield context
    context.close()

@pytest.fixture
def page(context):
    page = context.new_page()
    yield page
    page.close()

@pytest.fixture
def login_page(page):
    return LoginPage(page)

@pytest.fixture(scope="session")
def config(request):
    environment = request.config.getoption("--env")
    return ConfigReader(environment)
