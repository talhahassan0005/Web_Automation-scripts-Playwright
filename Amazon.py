import asyncio
from playwright.sync_api import sync_playwright, Playwright, expect
from playwright.async_api import async_playwright

AmazonProduct = []


def extractUrl(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(permissions=['geolocation'])
    requestsheaders = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Cookie': 'aws-target-data=%7B%22support%22%3A%221%22%7D; AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19626%7CMCMID%7C68172235662354508121040016482036576348%7CMCAAMLH-1696264569%7C3%7CMCAAMB-1696264569%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1695666970s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; aws-target-visitor-id=1695659770330-967514.48_0; aws-ubid-main=905-7000728-5824581; regStatus=registering; session-id=144-6827394-9346432; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn="L5Z9:PK"; ubid-main=135-0055847-8491515; session-token=UtlFSeeXp/3abYNXs2g9LOtF9D8g+Z0YgWoOJNljFLYS287UVzYULelehx8OzDObwyT9qu4kGl3+KhY1TPTGyFCvLDJOvcrnWyk1Ig1AGAmFwyOJgyz9eezUjuNyi1dzmX3tnBg3QBvu/Ct+rXsMsqkMlQFgc35RnIDvktcR7izDnyTC4FwNeNnJU1qOmcgGMdYKABLl93mNS5uRLNwprGgkfocezp8dgxTrb3KILHQsUiQTUIS+btRzOGsJYASjuhc7DRFSTCCDOiXkEEGx4O+1iZEW+3RqwN1WYg5keRMquDSW9bRkHPyswrp+RCFS+BPKxLqnL2q3MCRb0qFVorsJUj7Jzdqy; csm-hit=tb:s-91GJHM1CNAM5T8VWKRCB|1695756939497&t:1695756940905&adb:adblk_yes',
        'Device-Memory': '8',
        'Downlink': '10',
        'Dpr': '1.5',
        'Ect': '4g',
        'Referer': 'https://www.amazon.com/s?k=amazom&adgrpid=85279052327&hvadid=585479886698&hvdev=c&hvlocphy=1011084&hvnetw=g&hvqmt=e&hvrand=3556383438181193927&hvtargid=kwd-296458785041&hydadcr=29489_14573936&tag=hydglogoo-20&ref=pd_sl_8rpm1r24ct_e',
        'Rtt': '150',
        'Sec-Ch-Device-Memory': '8',
        'Sec-Ch-Dpr': '1.5',
        'Sec-Ch-Ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"14.0.0"',
        'Sec-Ch-Viewport-Width': '779',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    }
    # context.set_extra_http_headers(headers=requestsheaders)
    page = context.new_page()
    page.goto("https://www.amazon.com/")
    page.wait_for_timeout(4000)
    page.get_by_role("button", name="Submit").first.click()
    page.get_by_placeholder("Search Amazon").click()
    page.get_by_placeholder("Search Amazon").fill("HP laptop")
    page.get_by_placeholder("Search Amazon").press("Enter")
    page.wait_for_timeout(2000)
    product = page.query_selector_all(
        "div.sg-col-20-of-24.s-result-item.s-asin.sg-col-0-of-12.sg-col-16-of-20.sg-col.s-widget-spacing-small.sg-col-12-of-16")
    print(len(product))
    for data in product:
        links = data.query_selector("a.a-link-normal.s-no-outline")
        productlinks = "https://www.amazon.com" + links.get_attribute("href")
        AmazonProduct.append(productlinks)
    page.wait_for_timeout(20000)
    context.close()
    browser.close()


with sync_playwright() as playwright:
    extractUrl(playwright)
print(AmazonProduct)
# -----------------------------------------------------------------------------------------------------------------------
for url in AmazonProduct:
    def info(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(permissions=['geolocation'])
        page = context.new_page()
        page.goto(url)
        page.wait_for_timeout(4000)
        try:
            page.get_by_role("button", name="Submit").first.click()
            productname = page.query_selector("h1#title.a-size-large.a-spacing-none")
            print(productname.inner_text())
        except:
            pass
        context.close()
        browser.close()


    with sync_playwright() as playwright:
        info(playwright)
# -----------------------------------------------------------------------------------------------------------------------

