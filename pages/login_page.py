"""
Login Page Object Model
Encapsulates all interactions with the Login page.
"""
from pages.base_page import BasePage

class LoginPage(BasePage):
    EMAIL_INPUT    = "#email"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON   = "#login-button"

    def navigate_to(self):
        self.navigate("/login.html")

    def enter_email(self, email):
        self.page.fill(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.page.fill(self.PASSWORD_INPUT, password)

    def click_login(self):
        self.page.click(self.LOGIN_BUTTON)

    def login(self, email, password):
        self.navigate_to()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_on_mypage(self):
        return "mypage" in self.page.url
