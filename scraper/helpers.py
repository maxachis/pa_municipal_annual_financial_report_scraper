from typing import Optional

from playwright._impl._errors import Error
from playwright.async_api import async_playwright

from scraper.constants import BASE_URL, DISPLAY_REPORT_ID
from scraper.exceptions import InvalidOptionException
from scraper.models.option import OptionInfo


async def trigger_download(page):
    # Trigger the download via JavaScript call
    await page.evaluate("""
        $find('ctl00_ContentPlaceHolder1_rvReport').exportReport('EXCELOPENXML');
    """)


async def try_triggering_download(additional_attempts, page):
    async with page.expect_download(timeout=60000) as download_info:
        print("Waiting for report to download...")
        for attempts in range(additional_attempts):
            try:
                await trigger_download(page)
                return download_info
            except Error as e:
                if "The report or page is being updated" in str(e):
                    await wait(page)
                    print("Retrying...")
                else:
                    raise
        # Try one final time, raising if it fails
        await trigger_download(page)
        return download_info


async def get_option_info(
        option,
        valid_labels: Optional[list[str]] = None
) -> OptionInfo:
    """
    Get the value and label of an option
    :param option:
    :param valid_labels:
    :return:
    """
    value = await option.get_attribute("value")
    if value == "-1":
        raise InvalidOptionException
    label = await option.inner_text()
    if valid_labels is None:
        return OptionInfo(value=value, label=label)
    if label not in valid_labels:
        raise InvalidOptionException
    return OptionInfo(value=value, label=label)


async def get_options(page, select_id: str):
    # Get all options from a select
    return await page.locator(f"select#{select_id} option").all()


async def select(page, select_id: str, value: str, wait_after: bool = True):
    # Select from a select option
    await page.select_option(f"select#{select_id}", value)
    if wait_after:
        await wait(page)


async def wait(page):
    # Wait for 1 second
    await page.wait_for_timeout(1000)


async def load_page(p: async_playwright):
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.wait_for_load_state("networkidle")
    return page


async def display_report(page):
    # Click the Display Report button
    await page.click(f"input#{DISPLAY_REPORT_ID}")
    await wait(page)
