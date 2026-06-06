"""
Test Suite 2: Signup / Registration
Covers: Functional, Negative, Boundary, Property-based testing.

Oracle Strategy:
  - Valid signup   → redirect to mypage.html
  - Invalid signup → validation errors appear, no redirect
"""
import pytest
import random
import string
from pages.signup_page import SignupPage
from utils.helpers import future_date


def random_email():
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"testuser_{suffix}@example.com"


class TestSignupFunctional:
    """TC-S-01 to TC-S-03: Positive registration scenarios."""

    def test_TC_S_01_valid_normal_user_registration(self, page):
        """New normal user can register and is redirected to mypage."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("TestPass123")
        sp.fill_password_confirm("TestPass123")
        sp.fill_username("Test User")
        sp.select_rank("normal")
        sp.submit()
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url  # Oracle: successful registration → mypage

    def test_TC_S_02_valid_premium_user_registration(self, page):
        """New premium user can register and is redirected to mypage."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("TestPass123")
        sp.fill_password_confirm("TestPass123")
        sp.fill_username("Premium Tester")
        sp.select_rank("premium")
        sp.submit()
        page.wait_for_url("**/mypage.html", timeout=10000)
        assert "mypage" in page.url

    def test_TC_S_03_signup_page_title(self, page):
        """Signup page must have correct title."""
        sp = SignupPage(page)
        sp.navigate_to()
        assert "HOTEL PLANISPHERE" in page.title()


class TestSignupNegative:
    """TC-S-04 to TC-S-08: Invalid registration inputs."""

    def test_TC_S_04_mismatched_passwords_blocked(self, page):
        """Mismatched password and confirmation must be rejected."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("Password123")
        sp.fill_password_confirm("DifferentPass")
        sp.fill_username("Mismatch User")
        sp.submit()
        page.wait_for_timeout(1000)
        assert "mypage" not in page.url  # Oracle: no redirect on mismatch

    def test_TC_S_05_empty_email_blocked(self, page):
        """Missing email must block registration."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_password("Password123")
        sp.fill_password_confirm("Password123")
        sp.fill_username("No Email User")
        sp.submit()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_S_06_empty_username_blocked(self, page):
        """Missing username must block registration."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("Password123")
        sp.fill_password_confirm("Password123")
        sp.submit()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_S_07_invalid_email_format_blocked(self, page):
        """Email without domain is rejected by HTML5 validation."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email("invalidemail")
        sp.fill_password("Password123")
        sp.fill_password_confirm("Password123")
        sp.fill_username("Bad Email User")
        sp.submit()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url

    def test_TC_S_08_empty_form_blocked(self, page):
        """Submitting completely empty form is blocked."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.submit()
        page.wait_for_timeout(500)
        assert "mypage" not in page.url


class TestSignupBoundary:
    """TC-S-09 to TC-S-10: Boundary value analysis."""

    def test_TC_S_09_username_single_character(self, page):
        """Single character username — minimum boundary test."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("Password123")
        sp.fill_password_confirm("Password123")
        sp.fill_username("A")  # 1 char — min boundary
        sp.submit()
        page.wait_for_timeout(2000)
        # Oracle: accepted OR rejected — we record actual behavior
        result = "mypage" in page.url
        print(f"[BVA] 1-char username accepted: {result}")

    def test_TC_S_10_password_minimum_length(self, page):
        """Short 4-character password — boundary test."""
        sp = SignupPage(page)
        sp.navigate_to()
        sp.fill_email(random_email())
        sp.fill_password("ab12")
        sp.fill_password_confirm("ab12")
        sp.fill_username("Short Pass User")
        sp.submit()
        page.wait_for_timeout(2000)
        result = "mypage" in page.url
        print(f"[BVA] 4-char password accepted: {result}")


class TestSignupPropertyBased:
    """TC-S-11: Property-based / invariant testing."""

    def test_TC_S_11_valid_registration_always_lands_on_mypage(self, page):
        """Property: any valid new user registration must end on mypage. Tested 3 times."""
        sp = SignupPage(page)
        for i in range(3):
            pg = page.context.new_page()
            sp2 = SignupPage(pg)
            sp2.navigate_to()
            sp2.fill_email(random_email())
            sp2.fill_password("ValidPass99")
            sp2.fill_password_confirm("ValidPass99")
            sp2.fill_username(f"PropertyUser{i}")
            sp2.select_rank("normal")
            sp2.submit()
            pg.wait_for_url("**/mypage.html", timeout=10000)
            assert "mypage" in pg.url, f"Iteration {i}: Valid signup did not reach mypage"
            pg.close()
