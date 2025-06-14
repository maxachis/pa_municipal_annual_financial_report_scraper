from playwright._impl import _errors
from playwright.async_api import Page

from src.config import YEARS
from src.db.client import DatabaseClient
from src.scraper.constants import MUNI_SELECT_ID, YEAR_SELECT_ID
from src.scraper.models.name_id import NameID
from src.scraper.processors.year import YearProcessor
from src.scraper.exceptions import EntryExistsException, NoAFRException, InvalidOptionException
from src.scraper.helpers import get_option_info, get_options, select
from src.scraper.models.option import OptionInfo


class MunicipalityProcessor:

    def __init__(
        self,
        db_client: DatabaseClient,
        page: Page,
        county: NameID,
        municipality_option: OptionInfo
    ):
        self.db_client = db_client
        self.page = page
        self.county = county
        self.municipality_option = municipality_option
        self.municipality = self.db_client.get_municipality_info(
            self.county.id,
            self.municipality_option.label
        )

    async def run(self):
        # Check if all years scraped. If so, skip
        all_scraped = self.db_client.all_years_scraped(
            muni_id=self.municipality.id,
            county_id=self.county.id
        )
        if all_scraped:
            return
        self.municipality_option.report()
        await select(self.page, MUNI_SELECT_ID, self.municipality_option.value)
        year_options = await get_options(self.page, YEAR_SELECT_ID)
        for year_option in year_options:
            try:
                option_info = await get_option_info(year_option)
                if option_info.label not in YEARS:
                    continue
                year_processor = YearProcessor(
                    db_client=self.db_client,
                    page=self.page,
                    municipality=self.municipality,
                    county=self.county,
                    year_option=option_info
                )
                await year_processor.run()
            except (
                EntryExistsException,
                NoAFRException,
                InvalidOptionException,
                _errors.TimeoutError
            ):
                continue
