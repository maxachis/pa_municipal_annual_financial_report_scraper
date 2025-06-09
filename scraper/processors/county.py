from playwright.async_api import Page

from db.client import DatabaseClient
from scraper.constants import COUNTY_SELECT_ID, MUNI_SELECT_ID
from scraper.processors.municipality import MunicipalityProcessor
from scraper.exceptions import InvalidOptionException, EntryExistsException
from scraper.main import select, get_options, get_option_info
from scraper.models.option import OptionInfo


class CountyProcessor:

    def __init__(
        self,
        db_client: DatabaseClient,
        page: Page,
        county_option: OptionInfo
    ):
        self.county_option = county_option
        self.page = page
        self.db_client = db_client
        self.county = self.db_client.get_county_info(self.county_option.label)

    async def run(self):
        await select(self.page, COUNTY_SELECT_ID, self.county_option.value)
        self.county_option.report()
        muni_options = await get_options(self.page, MUNI_SELECT_ID)
        for muni_option in muni_options:
            muni_processor = MunicipalityProcessor(
                db_client=self.db_client,
                page=self.page,
                county=self.county,
                municipality_option=await get_option_info(muni_option)
            )
            try:
                await muni_processor.run()
            except (
                InvalidOptionException,
                EntryExistsException
            ):
                continue
