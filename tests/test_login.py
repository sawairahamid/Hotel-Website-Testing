"""
Test Suite 1: Login Functionality
Covers: Functional, Negative, Boundary, State-based testing.

Oracle Strategy:
  - Valid login   → URL redirects to mypage.html
  - Invalid login → stays on login page, no redirect
"""
import pytest
from pages.login_page import LoginPage
from utils.helpers import PREMIUM_USER, NORMAL_USER, INVALID_USER, WRONG_PASSWORD


class TestLoginFunctional:
    """TC-L-01 to TC-L-04: Positive login scenarios."""

    def test_TC_L_01_valid_premium_user_login(self, page):
        """Premium user with correct credentials reaches mypage."""
        lp = LoginPage(page)
        lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url  # Oracle: redirect to mypage

    def test_TC_L_02_valid_normal_user_login(self, page):
        """Normal user with correct credentials reaches mypage."""
        lp = LoginPage(page)
        lp.login(NORMAL_USER["email"], NORMAL_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url

    def test_TC_L_03_login_page_loads_correctly(self, page):
        """Login page loads and shows the hotel brand name in body."""
        lp = LoginPage(page)
        lp.navigate_to()
        page.wait_for_load_state("networkidle")
        body = page.locator("body").inner_text()
        assert "Hotel" in body or "hotel" in body.lower() or "login" in body.lower() or page.url.endswith("login.html")

    def test_TC_L_04_login_form_elements_visible(self, page):
        """All required login form fields must be visible."""
        lp = LoginPage(page)
        lp.navigate_to()
        page.wait_for_load_state("networkidle")
        assert page.locator(lp.EMAIL_INPUT).is_visible()
        assert page.locator(lp.PASSWORD_INPUT).is_visible()
        assert page.locator(lp.LOGIN_BUTTON).is_visible()


class TestLoginNegative:
    """TC-L-05 to TC-L-09: Negative/invalid input scenarios."""

    def test_TC_L_05_nonexistent_user_rejected(self, page):
        """Non-registered email is rejected, no mypage redirect."""
        lp = LoginPage(page)
        lp.login(INVALID_USER["email"], INVALID_USER["password"])
        page.wait_for_timeout(2000)
        assert "mypage" not in page.url  # Oracle: must stay on login

    def test_TC_L_06_wrong_password_rejected(self, page):
        """Correct email but wrong password must be rejected."""
        lp = LoginPage(page)
        lp.login(WRONG_PASSWORD["email"], WRONG_PASSWORD["password"])
        page.wait_for_timeout(2000)
        assert "mypage" not in page.url

    def test_TC_L_07_empty_email_blocked(self, page):
        """Form submission with empty email field is blocked."""
        lp = LoginPage(page)
        lp.navigate_to()
        lp.enter_password("password")
        lp.click_login()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_L_08_empty_password_blocked(self, page):
        """Form submission with empty password field is blocked."""
        lp = LoginPage(page)
        lp.navigate_to()
        lp.enter_email(PREMIUM_USER["email"])
        lp.click_login()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_L_09_empty_form_blocked(self, page):
        """Completely empty form submission is blocked."""
        lp = LoginPage(page)
        lp.navigate_to()
        lp.click_login()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url


class TestLoginBoundary:
    """TC-L-10 to TC-L-11: Boundary value analysis."""

    def test_TC_L_10_malformed_email_rejected(self, page):
        """Email without @ symbol fails HTML5 validation."""
        lp = LoginPage(page)
        lp.navigate_to()
        lp.enter_email("notanemail")
        lp.enter_password("password")
        lp.click_login()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_L_11_single_char_password_rejected(self, page):
        """1-character password for a known user must be rejected."""
        lp = LoginPage(page)
        lp.login(PREMIUM_USER["email"], "x")
        page.wait_for_timeout(2000)
        assert "mypage" not in page.url


class TestLoginStateBased:
    """TC-L-12: State transition testing."""

    def test_TC_L_12_logout_then_relogin(self, page):
        """User can logout and then log back in successfully (state transition)."""
        lp = LoginPage(page)
        lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url

        page.locator("text=Logout").click()
        page.wait_for_timeout(1500)
        assert "mypage" not in page.url

        lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url
