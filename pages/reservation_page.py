"""
Reservation Page Object Model
"""

class ReservationPage:
    DATE_INPUT           = "#date"
    TERM_INPUT           = "#term"
    HEAD_COUNT_INPUT     = "#head-count"
    BREAKFAST_CHECKBOX   = "#breakfast"
    EARLY_CHECKIN_CHECKBOX = "#early-check-in"
    SIGHTSEEING_CHECKBOX = "#sightseeing"
    USERNAME_INPUT       = "#username"
    CONTACT_SELECT       = "#contact"
    EMAIL_INPUT          = "#email"
    TEL_INPUT            = "#tel"
    COMMENT_AREA         = "#comment"
    TOTAL_BILL           = "#total-bill"
    SUBMIT_BUTTON        = "#submit-button"

    def __init__(self, page):
        self.page = page

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_selector(self.DATE_INPUT, timeout=10000)

    def set_date(self, d):       self.page.fill(self.DATE_INPUT, d)
    def set_term(self, n):       self.page.fill(self.TERM_INPUT, str(n))
    def set_head_count(self, n): self.page.fill(self.HEAD_COUNT_INPUT, str(n))
    def set_username(self, v):   self.page.locator(self.USERNAME_INPUT).fill(v)
    def set_comment(self, v):    self.page.fill(self.COMMENT_AREA, v)

    def toggle_breakfast(self, on=True):
        cb = self.page.locator(self.BREAKFAST_CHECKBOX)
        if cb.is_checked() != on: cb.click()

    def toggle_early_checkin(self, on=True):
        cb = self.page.locator(self.EARLY_CHECKIN_CHECKBOX)
        if cb.is_checked() != on: cb.click()

    def toggle_sightseeing(self, on=True):
        cb = self.page.locator(self.SIGHTSEEING_CHECKBOX)
        if cb.is_checked() != on: cb.click()

    def set_contact(self, method):
        self.page.select_option(self.CONTACT_SELECT, method)

    def set_email(self, v): self.page.fill(self.EMAIL_INPUT, v)
    def set_tel(self, v):   self.page.fill(self.TEL_INPUT, v)

    def get_total_price_text(self):
        self.page.wait_for_selector(self.TOTAL_BILL, timeout=6000)
        return self.page.locator(self.TOTAL_BILL).inner_text()

    def get_total_price_value(self):
        try:
            self.page.wait_for_selector(self.TOTAL_BILL, timeout=8000)
            text = self.page.locator(self.TOTAL_BILL).inner_text()
            digits = "".join(c for c in text if c.isdigit())
            return int(digits) if digits else 0
        except:
            return 0

    def submit(self):
        self.page.click(self.SUBMIT_BUTTON)

    def get_modal_text(self):
        self.page.wait_for_selector(".modal", timeout=8000)
        return self.page.locator(".modal-body").inner_text()

    def confirm_booking(self):
        self.page.locator(".modal .btn-primary").click()


    def get_total_price_value(self):
        try:
            self.page.wait_for_selector(self.TOTAL_BILL, timeout=8000)
            text = self.page.locator(self.TOTAL_BILL).inner_text()
            digits = "".join(c for c in text if c.isdigit())
            return int(digits) if digits else 0
        except:
            return 0

