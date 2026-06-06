"""
conftest.py — Shared pytest fixtures
"""
import pytest
from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from pages.signup_page import SignupPage
from pages.plans_page import PlansPage
from utils.helpers import PREMIUM_USER, NORMAL_USER


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        yield b
        b.close()

@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context()
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    pg = context.new_page()
    yield pg
    pg.close()

@pytest.fixture
def login_page(page):    return LoginPage(page)
@pytest.fixture
def signup_page(page):   return SignupPage(page)
@pytest.fixture
def plans_page(page):    return PlansPage(page)

@pytest.fixture
def logged_in_premium(page):
    lp = LoginPage(page)
    lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
    page.wait_for_url("**/mypage.html", timeout=10000)
    return page

@pytest.fixture
def logged_in_normal(page):
    lp = LoginPage(page)
    lp.login(NORMAL_USER["email"], NORMAL_USER["password"])
    page.wait_for_url("**/mypage.html", timeout=10000)
    return page
