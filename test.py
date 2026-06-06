from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=False)
    pg = b.new_page()
    pg.goto("https://hotel-example-site.takeyaqa.dev/en-US/signup.html")
    pg.wait_for_timeout(3000)
    input("Look at the page, then press Enter")
    b.close()