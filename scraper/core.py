from playwright.async_api import Page

from db.client import DatabaseClient
from scraper.constants import COUNTY_SELECT_ID, COUNTY_LABELS
from scraper.exceptions import InvalidOptionException
from scraper.helpers import get_option_info
from scraper.processors.county import CountyProcessor


class Scraper:
    
    def __init__(
        self,
        db_client: DatabaseClient,
        page: Page
    ):
        self.page = page
        self.db_client = db_client

    async def get_options(self, select_id: str):
        return await self.page.locator(f"select#{select_id} option").all()
        
    async def run(self):
        county_options = await self.get_options(COUNTY_SELECT_ID)
        for county_option in county_options:
            try:
                option_info = await get_option_info(county_option)
                if option_info.label not in COUNTY_LABELS:
                    continue
                county_processor = CountyProcessor(
                    db_client=self.db_client,
                    page=self.page,
                    county_option=await get_option_info(county_option)
                )
                await county_processor.run()
            except InvalidOptionException:
                continue
