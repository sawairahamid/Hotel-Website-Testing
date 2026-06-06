"""
Test Suite 4: Reservation / Booking Form
Covers: Functional, Boundary, Oracle (price calculation), E2E flow.

Oracle Strategy:
  - Price formula: base_rate × nights × guests [+ breakfast add-on + extras]
  - Confirmed booking modal must contain booking summary
  - Invalid guest count (0 or negative) must be rejected
"""
import pytest
from pages.plans_page import PlansPage
from pages.reservation_page import ReservationPage
from utils.helpers import future_date, boundary_values, PREMIUM_USER
from pages.login_page import LoginPage


def get_reservation_page(page):
    pp = PlansPage(page)
    pp.navigate_to()
    new_page = pp.click_reserve_on_plan(index=0)
    new_page.wait_for_load_state("networkidle")
    new_page.wait_for_timeout(2000)   # ← add this line
    rp = ReservationPage(new_page)
    rp.wait_for_load()
    return rp, new_page

class TestReservationFunctional:
    """TC-R-01 to TC-R-03: Reservation form structure and basic flow."""

    def test_TC_R_01_reservation_form_loads(self, page):
        """Reservation form opens with all required fields visible."""
        rp, new_page = get_reservation_page(page)
        assert new_page.locator(rp.DATE_INPUT).is_visible()
        assert new_page.locator(rp.TERM_INPUT).is_visible()
        assert new_page.locator(rp.HEAD_COUNT_INPUT).is_visible()
        assert new_page.locator(rp.SUBMIT_BUTTON).is_visible()
        new_page.close()

    def test_TC_R_02_total_price_displayed(self, page):
        """Total price element must be visible and non-empty."""
        rp, new_page = get_reservation_page(page)
        price_text = rp.get_total_price_text()
        assert price_text.strip() != "", "Total price must not be empty"
        new_page.close()

    def test_TC_R_03_date_field_accepts_future_date(self, page):
        """Reservation form accepts a future date without errors."""
        rp, new_page = get_reservation_page(page)
        rp.set_date(future_date(7))
        new_page.wait_for_timeout(500)
        # Oracle: no error message visible
        errors = new_page.locator(".invalid-feedback:visible")
        assert errors.count() == 0, "Future date should not cause validation error"
        new_page.close()


class TestReservationBoundary:
    """TC-R-04 to TC-R-07: Boundary value analysis for numeric fields."""

    def test_TC_R_04_head_count_minimum_1(self, page):
        """Guest count = 1 is the minimum valid value."""
        rp, new_page = get_reservation_page(page)
        rp.set_head_count(1)
        new_page.wait_for_timeout(500)
        val = new_page.locator(rp.HEAD_COUNT_INPUT).input_value()
        assert val == "1", f"Min head count should be 1, got {val}"
        new_page.close()

    def test_TC_R_05_head_count_zero_invalid(self, page):
        """Guest count = 0 is below minimum and must be rejected on submit."""
        rp, new_page = get_reservation_page(page)
        rp.set_date(future_date(3))
        rp.set_term(1)
        rp.set_head_count(0)  # BVA: below min
        rp.set_username("BVA Tester")
        rp.set_contact("email")
        rp.set_email("test@example.com")
        rp.submit()
        new_page.wait_for_timeout(1000)
        # Oracle: modal should NOT appear for invalid input
        modal_count = new_page.locator(".modal").count()
        assert modal_count == 0, "Modal must not appear for guest count = 0"
        new_page.close()

    def test_TC_R_06_term_minimum_1_night(self, page):
        """Stay duration of 1 night is minimum boundary."""
        rp, new_page = get_reservation_page(page)
        rp.set_term(1)
        new_page.wait_for_timeout(500)
        val = new_page.locator(rp.TERM_INPUT).input_value()
        assert val == "1", f"Min term should be 1, got {val}"
        new_page.close()

    def test_TC_R_07_term_zero_invalid(self, page):
        """Stay duration of 0 nights is invalid — below minimum boundary."""
        rp, new_page = get_reservation_page(page)
        rp.set_date(future_date(3))
        rp.set_term(0)  # BVA: below min
        rp.set_head_count(1)
        rp.set_username("BVA Tester")
        rp.set_contact("email")
        rp.set_email("test@example.com")
        rp.submit()
        new_page.wait_for_timeout(1000)
        modal_count = new_page.locator(".modal").count()
        assert modal_count == 0, "Modal must not appear for 0-night stay"
        new_page.close()


class TestReservationOracle:
    """TC-R-08 to TC-R-09: Price calculation oracle verification."""

    def test_TC_R_08_price_increases_with_more_nights(self, page):
        """
        Oracle Invariant: price for 2 nights must be greater than price for 1 night
        (same guests, no add-ons). Tests monotonic price scaling.
        """
        rp, new_page = get_reservation_page(page)
        rp.set_date(future_date(5))
        rp.set_head_count(1)

        rp.set_term(1)
        new_page.wait_for_timeout(1500)
        price_1_night = rp.get_total_price_value()

        rp.set_term(2)
        new_page.wait_for_timeout(1500)
        price_2_nights = rp.get_total_price_value()

        assert price_2_nights > price_1_night, (
            f"Oracle failed: 2-night price ({price_2_nights}) should exceed "
            f"1-night price ({price_1_night})"
        )
        new_page.close()

    def test_TC_R_09_price_increases_with_more_guests(self, page):
        """
        Oracle Invariant: price for 2 guests must be greater than price for 1 guest
        (same nights, no add-ons). Tests per-person scaling.
        """
        rp, new_page = get_reservation_page(page)
        rp.set_date(future_date(5))
        rp.set_term(1)

        rp.set_head_count(1)
        new_page.wait_for_timeout(1500)
        price_1_guest = rp.get_total_price_value()

        rp.set_head_count(2)
        new_page.wait_for_timeout(1500)
        price_2_guests = rp.get_total_price_value()

        assert price_2_guests > price_1_guest, (
            f"Oracle failed: 2-guest price ({price_2_guests}) should exceed "
            f"1-guest price ({price_1_guest})"
        )
        new_page.close()


class TestReservationE2E:
    """TC-R-10: End-to-end booking flow."""

    def test_TC_R_10_complete_booking_flow(self, page):
        """
        E2E: Login → Navigate to Plans → Select Plan → Fill Form → Submit → Confirm.
        Oracle: Confirmation modal appears with booking details.
        """
        # Step 1: Login
        lp = LoginPage(page)
        lp.login(PREMIUM_USER["email"], PREMIUM_USER["password"])
        page.wait_for_url("**/mypage.html", timeout=10000)

        # Step 2: Go to plans
        pp = PlansPage(page)
        pp.navigate_to()
        new_page = pp.click_reserve_on_plan(index=0)

        # Step 3: Fill reservation form
        rp = ReservationPage(new_page)
        rp.wait_for_load()
        rp.set_date(future_date(10))
        rp.set_term(2)
        rp.set_head_count(2)
        rp.set_username("Clark Kent")
        rp.set_contact("email")
        rp.set_email(PREMIUM_USER["email"])
        rp.set_comment("Automated E2E test booking")

        # Step 4: Submit
        rp.submit()

        # Step 5: Oracle — confirmation modal must appear
        modal_text = rp.get_modal_text()
        assert modal_text.strip() != "", "Oracle: Confirmation modal must appear after valid booking"
        new_page.close()
