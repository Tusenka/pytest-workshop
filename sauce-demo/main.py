import json
from functools import partialmethod
from inspect import getfullargspec
from urllib.parse import urljoin

import allure
import pytest
from _pytest.monkeypatch import MonkeyPatch
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options as FirefoxOption
from selenium.webdriver.chrome.options import Options as ChromeOption

#POM implementation
class LoginPage:
    def __init__(self, browser: WebDriver, config: dict):
        self.browser=browser
        self.config=config

    def login(self, username: str, password: str):
        self.browser.get(self.config['login_page'])
        login_field=self.browser.find_element(value=self.config['login_id'])
        login_field.send_keys(username)
        password_field=self.browser.find_element(value=self.config['password_id'])
        password_field.send_keys(password)
        self.browser.find_element(value=self.config['button_id']).click()

#TODO::
def screenshot_on_fail(browser_attr='browser'):
    def decorator(cls):
        def with_screen_shot(self, fn, *args, **kwargs):
            try:
                return fn(self, *args, **kwargs)
            except Exception:
                browser = getattr(args, browser_attr)
                filename = 'screenshot-%s.png' % fn.__name__
                browser.get_screenshot_as_file(filename)
                raise

        for attr, fn in cls.__dict__.items():
            if attr.startswith('test_') and callable(fn) and browser_attr in getfullargspec(fn).args:
                setattr(cls, attr, partialmethod(with_screen_shot, fn))

        return cls

    return decorator

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

@pytest.fixture(scope="function", autouse=True)
def pytest_browser_rel_path( browser, config, monkeypatch: MonkeyPatch):
        browser_get = browser.get

        def get_rel_url(rel_path: str):
            browser_get(urljoin(config['base_url'], rel_path))

        monkeypatch.setattr(browser, "get", get_rel_url)

class TestLogin():
    @pytest.fixture(scope="module", params=['Firefox', 'Chrome'], ids=["firefox", "chrome"])
    @allure.title("web driver")
    def browser(self, request: pytest.FixtureRequest):
        driver = None
        match request.param:
            case 'Firefox':
                options = FirefoxOption()
                options.add_argument('--headless')
                driver = webdriver.Firefox(options=options)
            case 'Chrome':
                options = ChromeOption()
                options.add_argument('--headless')
                driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.close()


    @pytest.fixture(scope="module")
    @allure.title("login page")
    def login_page(self, browser: WebDriver, config) ->WebDriver:
        yield LoginPage(browser, config)


    @allure.feature("Check login pathway")
    @allure.epic("Sauce Demo")
    @allure.tag("critical_path", "" , "login")
    @allure.description("This is the demo test for linux")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.link("https://www.saucedemo.com/", name="Sauce Demo")
    @allure.issue("JW-3.1.1")
    @pytest.mark.parametrize("username, password", [('standard_user', 'secret_sauce'),  ('problem_user', 'secret_sauce'),
                                                    ('performance_glitch_user','secret_sauce'),('error_user','secret_sauce')])
    def test_success_login_by_password(self, browser: WebDriver, login_page: LoginPage, config: dict, username: str, password: str):
        with allure.step(f"I login to swag as user {username} with password {password}"):
            login_page.login(username, password)
        with allure.step("And it cookies contains current user"):
            assert browser.get_cookies()[0]['value']==username
        with allure.step("And I am on inventory page"):
            assert browser.current_url==urljoin(config['base_url'], config['inventory_page'])

