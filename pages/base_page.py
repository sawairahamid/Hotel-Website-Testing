"""
Base Page Object Model
Provides common methods shared across all pages.
"""

BASE_URL = "https://hotel-example-site.takeyaqa.dev/en-US"

class BasePage:
    def __init__(self, page):
        self.page = page
        self.base_url = BASE_URL

    def navigate(self, path=""):
        self.page.goto(f"{self.base_url}{path}")

    def get_title(self):
        return self.page.title()

    def get_url(self):
        return self.page.url
