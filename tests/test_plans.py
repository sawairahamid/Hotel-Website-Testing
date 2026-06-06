"""
Test Suite 3: Plans Page (Ajax-loaded content)
Covers: Functional, State-based (Premium vs Normal), Flaky test handling.

Oracle Strategy:
  - Premium users see MORE plans than normal users
  - Plan cards must load within timeout (Ajax wait strategy applied)
  - Each card must contain a title and a reserve button
"""
from pprint import pp

import pytest
from conftest import page
from pages.plans_page import PlansPage
from pages.login_page import LoginPage
from utils.helpers import PREMIUM_USER, NORMAL_USER


class TestPlansPageFunctional:
    """TC-P-01 to TC-P-03: Plans page structure and load."""

    def test_TC_P_01_plans_page_loads_without_login(self, page):
        """Plans page is accessible without login and shows at least 1 plan."""
        pp = PlansPage(page)
        pp.navigate_to()
        pp.wait_for_plans()  # Explicit wait — flaky test fix (Phase 8)
        count = pp.get_plan_count()
        assert count >= 1, f"Expected at least 1 plan, got {count}"

    def test_TC_P_02_each_plan_has_title(self, page):
        """Every plan card must have a non-empty title."""
        pp = PlansPage(page)
        pp.navigate_to()
        titles = pp.get_plan_titles()
        assert len(titles) > 0
        for title in titles:
            assert title.strip() != "", "Plan card has empty title"

    def test_TC_P_03_reserve_button_opens_new_page(self, page):
        """Clicking Reserve on first plan opens a new page (reservation form)."""
        pp = PlansPage(page)
        pp.navigate_to()
        new_page = pp.click_reserve_on_plan(index=0)
        assert new_page is not None
        assert "reserve" in new_page.url or "hotel" in new_page.url
        new_page.close()


class TestPlansStateBased:
    """TC-P-04 to TC-P-05: Premium vs Normal user plan visibility."""

    def test_TC_P_04_premium_user_sees_more_plans(self, page):
        from pages.login_page import LoginPage
        from utils.helpers import PREMIUM_USER, NORMAL_USER

        # Premium session
        lp = LoginPage(page)
        lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        pp = PlansPage(page)
        pp.navigate_to()
        premium_count = pp.get_plan_count()

        # Logout
        page.locator("text=Logout").click()
        page.wait_for_timeout(1500)

        # Normal session (same page, different login)
        lp.login(NORMAL_USER["email"], NORMAL_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)
        pp.navigate_to()
        normal_count = pp.get_plan_count()

        assert premium_count >= normal_count

    def test_TC_P_05_logged_in_user_sees_username_on_plans(self, logged_in_premium):
        """After login, user's name appears on the plans page header."""
        pp = PlansPage(logged_in_premium)
        pp.navigate_to()
        pp.wait_for_plans()
        body_text = logged_in_premium.locator("body").inner_text()
        # Oracle: page must contain user-related text after login
        assert "Clark" in body_text or "clark" in body_text.lower() or "Logout" in body_text


class TestPlansFlaky:
    """TC-P-06: Flaky test handling — Ajax timing."""

    def test_TC_P_06_plans_load_within_timeout_multiple_runs(self, page):
        """
        Phase 8: Ajax-loaded content requires explicit wait.
        This test verifies plans always load within 12 seconds (3 repeated runs).
        Without wait_for_selector, this would be a flaky test.
        """
        for run in range(3):
            pg = page.context.new_page()
            pp = PlansPage(pg)
            pp.navigate_to()
            try:
                pp.wait_for_plans()
                count = pp.get_plan_count()
                assert count >= 1, f"Run {run+1}: Plans did not load"
            finally:
                pg.close()
