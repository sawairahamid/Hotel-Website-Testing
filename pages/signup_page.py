"""
Signup Page Object Model
"""
from pages.base_page import BasePage

class SignupPage(BasePage):
    EMAIL_INPUT            = "#email"
    PASSWORD_INPUT         = "#password"
    PASSWORD_CONFIRM_INPUT = "#password-confirmation"
    USERNAME_INPUT         = "#username"
    RANK_PREMIUM           = "#rank-premium"
    RANK_NORMAL            = "#rank-normal"
    ADDRESS_INPUT          = "#address"
    TEL_INPUT              = "#tel"
    GENDER_SELECT          = "#gender"
    BIRTHDAY_INPUT         = "#birthday"
    SUBMIT_BUTTON          = "button[type='submit']"

    def navigate_to(self):
        self.navigate("/signup.html")

    def fill_email(self, v):        self.page.fill(self.EMAIL_INPUT, v)
    def fill_password(self, v):     self.page.fill(self.PASSWORD_INPUT, v)
    def fill_password_confirm(self, v): self.page.fill(self.PASSWORD_CONFIRM_INPUT, v)
    def fill_username(self, v):     self.page.fill(self.USERNAME_INPUT, v)
    def fill_address(self, v):      self.page.fill(self.ADDRESS_INPUT, v)
    def fill_tel(self, v):          self.page.fill(self.TEL_INPUT, v)

    def select_rank(self, rank="normal"):
        if rank == "premium":
            self.page.click(self.RANK_PREMIUM)
        else:
            self.page.click(self.RANK_NORMAL)

    def select_gender(self, value):
        self.page.select_option(self.GENDER_SELECT, value)

    def fill_birthday(self, date):
        self.page.fill(self.BIRTHDAY_INPUT, date)

    def submit(self):
        self.page.click(self.SUBMIT_BUTTON)

    def get_validation_errors(self):
        errors = self.page.locator(".invalid-feedback")
        return [errors.nth(i).inner_text() for i in range(errors.count())]

    def register_user(self, email, password, username, rank="normal"):
        self.navigate_to()
        self.fill_email(email)
        self.fill_password(password)
        self.fill_password_confirm(password)
        self.fill_username(username)
        self.select_rank(rank)
        self.submit()
