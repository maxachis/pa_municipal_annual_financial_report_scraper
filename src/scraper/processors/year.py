import asyncio
from pathlib import Path

from playwright._impl import _errors
from playwright._impl._errors import Error
from playwright.async_api import Page

from src.db.client import DatabaseClient
from src.scraper.constants import DISPLAY_REPORT_ID, YEAR_SELECT_ID
from src.scraper.exceptions import NoAFRException
from src.scraper.helpers import select, wait, display_report
from src.scraper.models.name_id import NameID
from src.scraper.models.option import OptionInfo
from src.util import project_path


class YearProcessor:

    def __init__(
        self,
        db_client: DatabaseClient,
        page: Page,
        county: NameID,
        municipality: NameID,
        year_option: OptionInfo
    ):
        self.db_client = db_client
        self.page = page
        self.county = county
        self.municipality = municipality
        self.year_option = year_option
        self.year = int(self.year_option.label)
        self.report = self.db_client.get_report_id(
            self.county.id,
            self.municipality.id,
            self.year
        )

    async def display_report(self):
        await self.page.click(f"input#{DISPLAY_REPORT_ID}")
        await wait(self.page)

    async def wait_for_loading(self):
        # Wait the value of the Display Report button to change to "Loading..."
        display_report_value = await self.page.locator(
            f"input#{DISPLAY_REPORT_ID}"
        ).get_attribute("value")
        while display_report_value != "Loading...":
            print("Waiting for loading to complete...")
            # Check if #ContentPlaceHolder1_lblError has text content 'There is no AFR for the parameters you selected.'
            error_text = await self.page.locator(
                "#ContentPlaceHolder1_lblError"
            ).inner_text()
            if "There is no AFR for the parameters you selected." in error_text:
                print("There is no AFR for the parameters you selected.")
                self.db_client.add_scraper_error(
                    report_id=self.report.id,
                    error="There is no AFR for the parameters you selected."
                )
                self.db_client.mark_as_scraped(self.report.id)
                # If so, skip this entry
                raise NoAFRException

            display_report_value = await self.page.locator(
                f"input#{DISPLAY_REPORT_ID}"
            ).get_attribute("value")
            await asyncio.sleep(0.5)
        await wait(self.page)

    async def wait_for_report(self):
        try:
            if self.db_client.has_timeout_error(self.report.id):
                raise _errors.TimeoutError("Timeout while waiting for report to load")
            print("Waiting for report to load...")
            await self.page.wait_for_selector("#ctl00_ContentPlaceHolder1_rvReport_ctl05_ctl04_ctl00_ButtonImg")
            await wait(self.page)
        except _errors.TimeoutError:
            self.db_client.add_scraper_error(self.report.id, "Timeout while waiting for report to load")
            raise

    async def trigger_download(self):
        # Trigger the download via JavaScript call
        await self.page.evaluate(
            """
            $find('ctl00_ContentPlaceHolder1_rvReport').exportReport('EXCELOPENXML');
        """
        )

    async def try_triggering_download(self, additional_attempts):
        async with self.page.expect_download(timeout=60000) as download_info:
            print("Waiting for report to download...")
            for attempts in range(additional_attempts):
                try:
                    await self.trigger_download()
                    return download_info
                except Error as e:
                    if "The report or page is being updated" in str(e):
                        await wait(self.page)
                        print("Retrying...")
                    else:
                        raise
            # Try one final time, raising if it fails
            await self.trigger_download()
            return download_info

    async def save_download(self, download) -> Path:
        # Save the downloaded file to a specific path
        path = project_path(
            "downloads",
            f"report_"
            f"{self.county.name}_"
            f"{self.municipality.name}_"
            f"{self.year}.xlsx")
        print(f"Saving report to {path}")
        await download.save_as(path)
        return path

    async def download_and_save(self, additional_attempts: int = 2) -> Path:
        download_info = await self.try_triggering_download(additional_attempts)
        # Get the download object
        download = await download_info.value

        return await self.save_download(download)

    async def run(self):
        await select(self.page, YEAR_SELECT_ID, self.year_option.value)
        self.year_option.report()
        if self.db_client.is_scraped(self.report.id):
            return
        await select(self.page, YEAR_SELECT_ID, self.year_option.value, wait_after=False)
        await display_report(self.page)
        await self.wait_for_loading()
        await self.wait_for_report()
        path = await self.download_and_save()
        self.db_client.mark_as_scraped(
            report_id=self.report.id,
            filename=path.name
        )
