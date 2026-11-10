import os

import pytest
from selenium import webdriver

driver = None


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection: chrome or firefox"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="run the browser without a window"
    )


@pytest.fixture(scope="function")
def browserInstance(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    headless = request.config.getoption("headless")
    # Selenium Manager (Selenium 4.6+) downloads the matching driver, so no driver path is needed
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("-headless")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=options)
    else:
        raise pytest.UsageError(f"Unsupported --browser_name: {browser_name}")

    driver.implicitly_wait(5)
    driver.get("https://rahulshettyacademy.com/loginpagePractise/")
    yield driver  # before test function execution
    driver.quit()  # after test function execution
    driver = None


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    Extends the pytest-html plugin to take and embed a screenshot in the HTML report whenever a test fails.
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when in ("call", "setup"):
        xfail = hasattr(report, "wasxfail")
        if ((report.skipped and xfail) or (report.failed and not xfail)) and driver is not None:
            reports_dir = os.path.join(os.path.dirname(__file__), "reports")
            os.makedirs(reports_dir, exist_ok=True)
            file_name = os.path.join(reports_dir, report.nodeid.replace("::", "_").replace("/", "_") + ".png")
            print("file name is " + file_name)
            _capture_screenshot(file_name)
            if pytest_html is not None:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extras.append(pytest_html.extras.html(html))
        report.extras = extras


def _capture_screenshot(file_name):
    driver.get_screenshot_as_file(file_name)
