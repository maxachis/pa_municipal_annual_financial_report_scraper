import asyncio

from aiohttp import ClientSession

from src.census.api.constants import CENSUS_API_URL
from src.census.api.model import CensusData
from environs import Env

class CensusScraper:

    def __init__(
        self,
        api_key: str,
        session: ClientSession
    ):
        self.api_key = api_key
        self.session = session


    async def get_data(
        self,
        year: int
    ) -> list[CensusData]:
        processed_data: list[CensusData] = []
        url: str = CENSUS_API_URL.format(YEAR=year, KEY=self.api_key)
        async with self.session.get(url) as response:
            raw_data: list[list[str]] = await response.json()
        for row in raw_data[1:]:
            census_data = CensusData(
                geo_id=row[0],
                name=row[1],
                population=int(row[2]),
                county_id=int(row[4]),
                municipality_id=int(row[5]),
            )
            processed_data.append(census_data)
        return processed_data

async def main():
    env = Env()
    env.read_env()

    async with ClientSession() as session:
        scraper = CensusScraper(
            api_key=env.str("CENSUS_API_KEY"),
            session=session
        )
        data = await scraper.get_data(year=2016)
        print(data)

if __name__ == "__main__":
    asyncio.run(main())