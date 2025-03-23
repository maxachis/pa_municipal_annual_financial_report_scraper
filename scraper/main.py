import asyncio
from typing import Optional

from playwright._impl import _errors
from playwright._impl._errors import Error
from playwright.async_api import async_playwright

from JsonCache import JsonCache
from constants import DISPLAY_REPORT_ID, YEAR_SELECT_ID, MUNI_SELECT_ID, COUNTY_SELECT_ID, BASE_URL
from config import COUNTIES, YEARS
from data_objects import CMY, OptionInfo
from exceptions import NoAFRException, InvalidOptionException, EntryExistsException


async def trigger_download(page):
    # Trigger the download via JavaScript call
    await page.evaluate("""
        $find('ctl00_ContentPlaceHolder1_rvReport').exportReport('EXCELOPENXML');
    """)

async def download_and_save(page, cmy: CMY, additional_attempts: int = 2):
    async with page.expect_download(timeout=60000) as download_info:
        print("Waiting for report to download...")
        for attempts in range(additional_attempts):
            try:
                await trigger_download(page)
                return
            except Error as e:
                if "The report or page is being updated" in str(e):
                    await wait(page)
                    print("Retrying...")
                else:
                    raise
        # Try one final time, raising if it fails
        await trigger_download(page)



    # Get the download object
    download = await download_info.value

    await save_download(download, cmy)

async def get_option_info(
        option,
        valid_labels: Optional[list[str]] = None
) -> OptionInfo:
    value = await option.get_attribute("value")
    if value == "-1":
        raise InvalidOptionException
    label = await option.inner_text()
    if valid_labels is None:
        return OptionInfo(value=value, label=label)
    if label not in valid_labels:
        raise InvalidOptionException
    return OptionInfo(value=value, label=label)


async def wait_for_report(page, cache: JsonCache, cmy: CMY):
    # Wait for #ctl00_ContentPlaceHolder1_rvReport_ctl05_ctl04_ctl00_ButtonImg to be visible
    try:
        print("Waiting for report to load...")
        await page.wait_for_selector("#ctl00_ContentPlaceHolder1_rvReport_ctl05_ctl04_ctl00_ButtonImg")
        await wait(page)
    except _errors.TimeoutError:
        cache.add_scraper_error(cmy=cmy, error="Timeout while waiting for report to load")
        raise


async def wait_for_loading(page, cache: JsonCache, cmy: CMY):
    # Wait the value of the Display Report button to change to "Loading..."
    display_report_value = await page.locator(f"input#{DISPLAY_REPORT_ID}").get_attribute("value")
    while display_report_value != "Loading...":
        print("Waiting for loading to complete...")
        # Check if #ContentPlaceHolder1_lblError has text content 'There is no AFR for the parameters you selected.'
        error_text = await page.locator("#ContentPlaceHolder1_lblError").inner_text()
        if "There is no AFR for the parameters you selected." in error_text:
            print("There is no AFR for the parameters you selected.")
            cache.add_scraper_error(
                cmy=cmy,
                error="There is no AFR for the parameters you selected."
            )
            cache.mark_as_scraped(cmy=cmy)
            # If so, skip this entry
            raise NoAFRException

        display_report_value = await page.locator(f"input#{DISPLAY_REPORT_ID}").get_attribute("value")
        await asyncio.sleep(0.5)
    await wait(page)

async def get_options(page, select_id: str):
    return await page.locator(f"select#{select_id} option").all()

async def select(page, select_id: str, value: str, wait_after: bool = True):
    await page.select_option(f"select#{select_id}", value)
    if wait_after:
        await wait(page)

async def wait(page):
    await page.wait_for_timeout(1000)

async def save_download(download, cmy: CMY):
    # Save the downloaded file to a specific path
    await download.save_as(f"downloads/report_{cmy.county}_{cmy.municipality}_{cmy.year}.xlsx")

async def get_option_value(option):
    return await option.get_attribute("value")

async def load_page(p: async_playwright):
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.wait_for_load_state("networkidle")
    return page

async def display_report(page):
    await page.click(f"input#{DISPLAY_REPORT_ID}")
    await wait(page)

async def main(cache: JsonCache):

    async with async_playwright() as p:
        page = await load_page(p)
        await county_loop(cache, page)

async def county_loop_iteration(cache: JsonCache, page, county_option):
    county_option_info = await get_option_info(county_option, COUNTIES)
    cmy = CMY(county=county_option_info.label)
    await select(page, COUNTY_SELECT_ID, county_option_info.value)
    county_option_info.report()
    await muni_loop(cache, cmy, page)

async def county_loop(cache: JsonCache, page):
    county_options = await get_options(page, COUNTY_SELECT_ID)
    for county_option in county_options:
        try:
            await county_loop_iteration(cache, page, county_option)
        except InvalidOptionException:
            continue


async def muni_loop_iteration(cache: JsonCache, cmy: CMY, page, muni_option):
    muni_option_info = await get_option_info(muni_option)
    cmy.municipality = muni_option_info.label
    if cache.all_municipalities_scraped(cmy):
        raise EntryExistsException
    muni_option_info.report()
    await select(page, MUNI_SELECT_ID, muni_option_info.value)
    await year_loop(cache, cmy, page)

async def muni_loop(cache: JsonCache, cmy: CMY, page):
    muni_options = await get_options(page, MUNI_SELECT_ID)
    for muni_option in muni_options:
        try:
            await muni_loop_iteration(cache, cmy, page, muni_option)
        except (
            EntryExistsException,
            InvalidOptionException
        ):
            continue


async def year_loop_iteration(cache: JsonCache, cmy: CMY, page, year_option):
    year_option_info = await get_option_info(
        option=year_option,
        valid_labels=YEARS
    )
    cmy.year = year_option_info.label
    if cache.is_scraped(cmy):
        raise EntryExistsException
    year_option_info.report()
    await select(page, YEAR_SELECT_ID, year_option_info.value, wait_after=False)
    await display_report(page)
    await wait_for_loading(page, cache, cmy)
    await wait_for_report(page=page, cache=cache, cmy=cmy)
    await download_and_save(page, cmy)

    cache.mark_as_scraped(cmy=cmy)

async def year_loop(cache: JsonCache, cmy: CMY, page):
    year_options = await get_options(page, YEAR_SELECT_ID)
    for year_option in year_options:
        try:
            await year_loop_iteration(cache, cmy, page, year_option)
        except (
                EntryExistsException,
                NoAFRException,
                InvalidOptionException,
                _errors.TimeoutError
        ):
            continue



if __name__ == "__main__":
    cache = JsonCache("../cache.json")
    cache.load_cache()
    max_additional_attempts = 5
    for i in range(max_additional_attempts):
        try:
            asyncio.run(main(cache))
            exit(0)
        except Exception as e:
            cache.save_cache()
            print(f"Error: {e}. Restarting ({max_additional_attempts - i} attempts left).")
    asyncio.run(main(cache))


