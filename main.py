import asyncio
import json
from pathlib import Path

from playwright._impl import _errors
from playwright._impl._errors import Error
from playwright.async_api import async_playwright

BASE_URL = "https://apps.dced.pa.gov/munstats-public/ReportInformation2.aspx?report=mAfrForm"

COUNTY_SELECT_ID = "ContentPlaceHolder1_ddCountyId"
MUNI_SELECT_ID = "ContentPlaceHolder1_ddMuniId"
YEAR_SELECT_ID = "ContentPlaceHolder1_ddYear"
DISPLAY_REPORT_ID = "ContentPlaceHolder1_btnDisplay"

YEARS = ["2015", "2016", "2017", "2018", "2019"]
COUNTIES = [
    "ALLEGHENY",
    "ARMSTRONG",
    "BEAVER",
    "BUTLER",
    "FAYETTE",
    "GREENE",
    "INDIANA",
    "LAWRENCE",
    "WESTMORELAND",
    "WASHINGTON"
]

class JsonCache:
    def __init__(self, filename: str):
        self.filename = filename
        self.cache = {}

    def add_entry(self, county: str, municipality: str, year: str, data):
        """Add an entry to the cache."""
        self.cache.setdefault(county, {}).setdefault(municipality, {})[year] = data

    def has_all_municipality_entries(self, county: str, municipality: str):
        d = self.cache.get(county, {}).get(municipality)
        if not d:
            return False
        return len(d.keys()) == len(YEARS)

    def get_entry(self, county: str, municipality: str, year: str):
        """Retrieve an entry from the cache."""
        return self.cache.get(county, {}).get(municipality, {}).get(year)

    def save_cache(self):
        """Save the cache to a JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=4)

    def load_cache(self):
        """Load the cache from a JSON file."""
        path = Path(self.filename)
        if path.exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}


async def get_options(page, select_id):
    return await page.locator(f"select#{select_id} option").all()

async def select(page, select_id, value):
    await page.select_option(f"select#{select_id}", value)

async def wait(page):
    await page.wait_for_timeout(1000)
    # await page.wait_for_load_state("networkidle")

async def main(cache: JsonCache):

    # Load page
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(BASE_URL)
        await page.wait_for_load_state("networkidle")

        # Get all counties from select with id "ContentPlaceHolder1_ddCountyId"
        # TODO: Refactor this section
        county_options = await get_options(page, COUNTY_SELECT_ID)

        for county_option in county_options:
            county_value = await county_option.get_attribute("value")
            if county_value == "-1":
                continue
            county_label = await county_option.inner_text()
            if county_label not in COUNTIES:
                continue

            await select(page, COUNTY_SELECT_ID, county_value)

            await wait(page)

            print(f"Value: {county_value}, Label: {county_label}")

            muni_options = await get_options(page, MUNI_SELECT_ID)

            for muni_option in muni_options:
                muni_value = await muni_option.get_attribute("value")
                if muni_value == "-1":
                    continue

                muni_label = await muni_option.inner_text()
                if cache.has_all_municipality_entries(county_label, muni_label):
                    continue

                print(f"Value: {muni_value}, Label: {muni_label}")
                await select(page, MUNI_SELECT_ID, muni_value)
                await wait(page)

                year_options = await get_options(page, YEAR_SELECT_ID)

                for year_option in year_options:
                    year_value = await year_option.get_attribute("value")
                    if year_value == "-1":
                        continue
                    year_label = await year_option.inner_text()
                    if cache.get_entry(county_label, muni_label, year_label):
                        continue
                    if year_label not in YEARS:
                        continue
                    print(f"Value: {year_value}, Label: {year_label}")
                    await select(page, YEAR_SELECT_ID, year_value)
                    await wait(page)

                    # Click "Display Report"
                    await page.click(f"input#{DISPLAY_REPORT_ID}")
                    await wait(page)

                    # Wait the value of the Display Report button to change to "Loading..."
                    display_report_value = await page.locator(f"input#{DISPLAY_REPORT_ID}").get_attribute("value")
                    while display_report_value != "Loading...":
                        print("Waiting for report to load...")
                        display_report_value = await page.locator(f"input#{DISPLAY_REPORT_ID}").get_attribute("value")
                        await asyncio.sleep(0.5)

                    await wait(page)

                    # Wait for #ctl00_ContentPlaceHolder1_rvReport_ctl05_ctl04_ctl00_ButtonImg to be visible
                    try:
                        print("Waiting for report to load...")
                        await page.wait_for_selector("#ctl00_ContentPlaceHolder1_rvReport_ctl05_ctl04_ctl00_ButtonImg")
                    except _errors.TimeoutError:
                        cache.add_entry(
                            county=county_label,
                            municipality=muni_label,
                            year=year_label,
                            data={"error": "Timeout while waiting for report to load"}
                        )
                        continue

                    await wait(page)

                    async with page.expect_download(timeout=60000) as download_info:
                        print("Waiting for report to download...")
                        # Trigger the download via JS call
                        try:
                            await page.evaluate("""
                                $find('ctl00_ContentPlaceHolder1_rvReport').exportReport('EXCELOPENXML');
                            """)
                        except Error:
                            if "The report or page is being updated" in str(Error):
                                await wait(page)
                                await page.evaluate("""
                                    $find('ctl00_ContentPlaceHolder1_rvReport').exportReport('EXCELOPENXML');
                                """)

                    # Get the download object
                    download = await download_info.value

                    # Save the downloaded file to a specific path
                    await download.save_as(f"downloads/report_{county_label}_{muni_label}_{year_label}.xlsx")

                    cache.add_entry(
                        county=county_label,
                        municipality=muni_label,
                        year=year_label,
                        data=True
                    )
                    cache.save_cache()







        # TODO: Next do municipalities

        # TODO: Next do years

        # TODO: Next do `Display Report` select

        # TODO: Add filtering by county and year

        # TODO: Add caching to track results.

        # TODO: Add download


if __name__ == "__main__":
    cache = JsonCache("cache.json")
    cache.load_cache()
    try:
        asyncio.run(main(cache))
    except Exception as e:
        cache.save_cache()
        raise e


