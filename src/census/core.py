import asyncio

from aiohttp import ClientSession
from environs import Env

from src.census.api.core import CensusScraper
from src.census.api.model import CensusData
from src.census.convert import convert_census_data_to_census_county, convert_census_data_to_census_municipality, \
    convert_census_data_to_census_municipality_pop
from src.config import YEARS
from src.db.client import DatabaseClient
from src.db.models.sqlalchemy.impl.census.county import CensusCounty
from src.db.models.sqlalchemy.impl.census.municipality import CensusMunicipality
from src.db.models.sqlalchemy.impl.census.municipality_population import CensusMunicipalityPopulation


async def process_year(
    scraper: CensusScraper,
    year: int,
    db_client: DatabaseClient
) -> None:
    data: list[CensusData] = await scraper.get_data(year=year)
    if year == 2015:
        census_counties: list[CensusCounty] = convert_census_data_to_census_county(data)
        census_municipalities: list[CensusMunicipality] = convert_census_data_to_census_municipality(data)
        db_client.add_all(census_counties)
        db_client.add_all(census_municipalities)
    census_municipality_pops: list[CensusMunicipalityPopulation] = (
        convert_census_data_to_census_municipality_pop(data, year)
    )
    db_client.add_all(census_municipality_pops)


async def main():
    env = Env()
    env.read_env()

    dbc = DatabaseClient()

    async with ClientSession() as session:
        scraper = CensusScraper(
            api_key=env.str("CENSUS_API_KEY"),
            session=session
        )

        for year in YEARS:
            await process_year(
                scraper=scraper,
                year=int(year),
                db_client=dbc
            )

if __name__ == "__main__":
    asyncio.run(main())