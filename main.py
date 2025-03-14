import asyncio
from playwright.async_api import async_playwright

BASE_URL = "https://apps.dced.pa.gov/munstats-public/ReportInformation2.aspx?report=mAfrForm"

async def main():

    # Load page
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")

        # Get all counties from select with id "ContentPlaceHolder1_ddCountyId"
        # TODO: Refactor this section
        # TODO: Make the ID a constant
        options = await page.locator("select#ContentPlaceHolder1_ddCountyId option").all()
        print(options)

        for option in options:
            value = await option.get_attribute("value")
            label = await option.inner_text()

            print(f"Value: {value}, Label: {label}")

            await page.select_option("select#ContentPlaceHolder1_ddCountyId", value)

            await page.wait_for_timeout(1000)
            await page.wait_for_load_state("networkidle")

        # TODO: Next do municipalities

        # TODO: Next do years

        # TODO: Next do `Display Report` select

        # TODO: Add filtering by county and year

        # TODO: Add caching to track results.

        # TODO: Add download


if __name__ == "__main__":
    asyncio.run(main())


