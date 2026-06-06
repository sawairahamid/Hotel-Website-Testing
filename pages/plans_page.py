"""
Plans Page Object Model
"""
from pages.base_page import BasePage

class PlansPage(BasePage):
    PLAN_CARDS      = ".card"
    PLAN_TITLES     = ".card-title"
    RESERVE_BUTTONS = ".btn-primary"

    def navigate_to(self):
        self.navigate("/plans.html")

    def wait_for_plans(self):
        self.page.wait_for_selector(self.PLAN_CARDS, timeout=12000)

    def get_plan_count(self):
        self.wait_for_plans()
        return self.page.locator(self.PLAN_CARDS).count()

    def get_plan_titles(self):
        self.wait_for_plans()
        cards = self.page.locator(self.PLAN_TITLES)
        return [cards.nth(i).inner_text() for i in range(cards.count())]

    def click_reserve_on_plan(self, index=0):
        self.wait_for_plans()
        with self.page.context.expect_page() as new_page_info:
            self.page.locator(self.RESERVE_BUTTONS).nth(index).click()
        new_page = new_page_info.value
        new_page.wait_for_load_state("networkidle")
        return new_page
