from playwright.sync_api import sync_playwright, Playwright, expect
import re
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup

def run(playwright: Playwright)-> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.google.com/")
    page.wait_for_timeout(2000)
    page.get_by_label(text="Search", exact=True).click()
    page.get_by_label(text="Search", exact=True).fill("Booking commerce")
    page.keyboard.press("Enter")

    page.get_by_role("link", name="Booking.com - Commerce Booking.com https://www.booking.com › commerce").click()
    page.get_by_label("Dismiss sign in information.").click()
    page.wait_for_timeout(2000)
    page.get_by_test_id("date-display-field-start").click()
    page.get_by_label("27 September 2023").click()
    page.get_by_label("31 October 2023").click()
    page.wait_for_timeout(2000)
    page.get_by_test_id("occupancy-config").click()
    page.locator("div").filter(has_text=re.compile(r"^2$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^3$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^4$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^0$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^Children1$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^1$")).locator("button").nth(1).click()
    page.locator("div").filter(has_text=re.compile(r"^Rooms2$")).locator("button").nth(1).click()
    page.get_by_role("combobox").first.select_option("7")
    page.get_by_role("combobox").nth(1).select_option("7")
    page.get_by_role("button", name="Done").click()
    page.wait_for_timeout(2000)
    page.get_by_placeholder("Where are you going?").click()
    page.keyboard.press("Shift+A")
    page.keyboard.press("Backspace")
    page.get_by_placeholder("Where are you going?").fill("NewYork")
    # page.query_selector('//*[@id="filter_group_popular_:r97:"]/div[4]').click()
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Search").click()


    # for pagination in range(3):
    #     page.keyboard.press("PageDown")
    #     page.wait_for_timeout(3000)
    #     page.keyboard.press("PageDown")
    #     page.wait_for_timeout(3000)
    #     page.keyboard.press("PageDown")
    #     page.wait_for_timeout(3000)

        # html = page.inner_html('div.rlt-right.maps-overlay-sr-container')
        # soup = BeautifulSoup(html, 'html.parser')
        # product = soup.find_all('div', {'data-testid': 'property-card'})
        # print(len(product))
        # html = HTMLParser(page.content())
        # print(html.css_first("div.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.da89aeb942").text())
        # product= page.query_selector_all("div.c82435a4b8.a178069f51.a6ae3c2b40.a18aeea94d.d794b7a0f7.f53e278e95.da89aeb942")
        # print(len(product))
        # for data in product:
        #     name = data.query_selector('[class="f6431b446c a23c043802"]')
        #     links = data.query_selector('a.e13098a59f')
        #     print(links.get_attribute("href"))
        #     print(name.inner_text())
        # page.get_by_label("Next page").click()
        #page.wait_for_timeout(20000)

    # page.wait_for_timeout(10000)
    context.close()
    browser.close()
with sync_playwright() as playwright:
    run(playwright)
