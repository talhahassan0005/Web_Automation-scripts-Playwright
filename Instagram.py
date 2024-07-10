import pandas as pd
from playwright.sync_api import sync_playwright, Playwright
from playwright.async_api import async_playwright
import asyncio

Main_categories_links = []


def categories(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://esupplier.pk/?page_id=15189")
    page.wait_for_timeout(3000)
    categories = page.query_selector_all(
        'xpath=//html/body/div[1]/div/div[2]/div/div/div/main/div/div/div/div[2]/div/section/div/ul/li[.]')
    print(len(categories))
    for cate_links in categories:
        links = cate_links.query_selector('a')
        Main_categories_links.append(links.get_attribute("href"))
    page.wait_for_timeout(5000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    categories(playwright)
print(Main_categories_links)
print(len(Main_categories_links))
print("#----------")
# -----------------------------------------------------------------------------------------------------------------------

second_links = []


async def sub_categories(sublink):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(sublink)
        await page.wait_for_timeout(3000)
        await page.reload()
        await page.wait_for_timeout(3000)
        product_links = await page.query_selector_all(
            "xpath=//html/body/div[1]/div/div[2]/div/div/div[1]/main/ul/li[.]/div/div/div[1]/a[1]")
        print(len(product_links))
        for exact_link in product_links:
            print(await exact_link.get_attribute("href"))
            second_links.append(await exact_link.get_attribute("href"))

        await context.close()
        await browser.close()


async def main():
    for sublink in Main_categories_links:
        await sub_categories(sublink)
asyncio.run(main())
#----------------------
print(second_links)
#------------------
print(len(second_links))
# ---------------------------------------------------------------------------------------------------------------------

product_list = []


async def info(data):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(data)
        await page.wait_for_timeout(3000)

        await page.wait_for_selector("h1.product_title.entry-title")

        categories = await page.query_selector("xpath=//html/body/div[1]/div/div[2]/div/nav/a[2]")
        print("Categories : ", await categories.inner_text())

        sub_categories = []
        try:
            sub_categories_element = await page.query_selector("xpath=//html/body/div[1]/div/div[2]/div/nav/a[3]")
            print("SubCategories : ", await sub_categories_element.inner_text())
            sub_categories.append(await sub_categories_element.inner_text())
        except Exception as e:
            sub_categories.append("NO subcategories")
            pass
        name_element = await page.query_selector("h1.product_title.entry-title")
        print("Name : ", await name_element.inner_text())
        categories_info = {
            "Categories": await categories.inner_text(),
            "SubCategories": sub_categories,
            "Name": await name_element.inner_text()
        }
        product_list.append(categories_info)
        await context.close()
        await browser.close()


# -----------------------------------------------------------------------------------------------------------------------
async def main():
    for data in second_links:
        await info(data)
asyncio.run(main())
# -----------------------------------------------------------------------------------------------------------------------

df = pd.DataFrame(product_list)
print(df)
df.to_csv('cate001.csv')
