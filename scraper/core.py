from playwright.async_api import Page

from db.client import DatabaseClient
from scraper.constants import COUNTY_SELECT_ID
from scraper.exceptions import InvalidOptionException
from scraper.main import get_option_info
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
            county_processor = CountyProcessor(
                db_client=self.db_client,
                page=self.page,
                county_option=await get_option_info(county_option)
            )
            try:
                await county_processor.run()
            except InvalidOptionException:
                continue
