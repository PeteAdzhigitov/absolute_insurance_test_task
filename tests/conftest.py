import pytest
from selenium.webdriver import Chrome
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.chrome.options import Options
import allure

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    driver = Chrome(options=options)
    driver.get("https://old.absolutins.ru/kupit-strahovoj-polis/strahovanie-zhizni-i-zdorovya/zashchita-ot-virusa/")
    yield driver

    tear_down(driver)

def tear_down(driver):
    driver.close()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed and item.funcargs.get('driver') is not None:
        page = item.funcargs['driver']

        screenshot = page.get_screenshot_as_png()

        allure.attach(
            screenshot,
            name=f"{item}.png".replace(" ", "_"),
            attachment_type=allure.attachment_type.PNG
        )