"""
Test Suite 5: My Page (Authenticated User Profile)
Covers: Functional, State-based, Negative (unauthorized access).

Oracle Strategy:
  - Logged-in user → sees their profile info on mypage
  - Non-logged-in user → redirected away from mypage
  - Premium user → sees "Premium" rank displayed
  - Normal user  → sees "Normal" rank displayed
"""
import pytest
from pages.login_page import LoginPage
from utils.helpers import PREMIUM_USER, NORMAL_USER, BASE_URL


class TestMyPageFunctional:
    """TC-M-01 to TC-M-03: Mypage content after login."""

    def test_TC_M_01_premium_user_mypage_accessible(self, logged_in_premium):
        """Premium user can access mypage after login."""
        assert "mypage" in logged_in_premium.url

    def test_TC_M_02_normal_user_mypage_accessible(self, logged_in_normal):
        """Normal user can access mypage after login."""
        assert "mypage" in logged_in_normal.url

    def test_TC_M_03_mypage_contains_user_info(self, logged_in_premium):
        """Mypage must display the logged-in user's information."""
        body = logged_in_premium.locator("body").inner_text()
        # Oracle: page contains some user-related identifiable content
        assert any(kw in body for kw in ["clark", "Clark", "Premium", "Logout"]), \
            "Mypage must show user info or logout option"


class TestMyPageStateBased:
    """TC-M-04 to TC-M-05: Role-based state differences."""

    def test_TC_M_04_premium_rank_shown(self, logged_in_premium):
        """Oracle: Premium member's page must indicate Premium rank."""
        body = logged_in_premium.locator("body").inner_text().lower()
        assert "premium" in body, "Premium user should see 'Premium' rank on mypage"

    def test_TC_M_05_normal_rank_shown(self, logged_in_normal):
        """Oracle: Normal member's page must indicate Normal rank."""
        body = logged_in_normal.locator("body").inner_text().lower()
        assert "normal" in body, "Normal user should see 'Normal' rank on mypage"


class TestMyPageNegative:
    """TC-M-06: Unauthorized access protection."""

    def test_TC_M_06_unauthenticated_user_cannot_access_mypage(self, page):
        """
        Non-logged-in user visiting mypage directly should be redirected.
        Oracle: mypage content must not be shown to unauthenticated users.
        """
        page.goto(f"{BASE_URL}/mypage.html")
        page.wait_for_timeout(2000)
        # Oracle: either redirected to login or mypage content gated
        current_url = page.url
        body = page.locator("body").inner_text().lower()
        is_protected = ("login" in current_url) or ("email" in body and "password" in body) or \
                       ("mypage" not in current_url)
        assert is_protected, "Unauthenticated users must not freely access mypage"
