from typing import Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models.pydantic.cache_entry import CacheEntry
from db.models.sqlalchemy.instantiations import County, Municipality, AnnualReport, ScrapeInfo, ProcessInfo, \
    ScrapeError, ProcessError
from db.queries.base import QueryBuilder


class ConvertStateToDBQueryBuilder(QueryBuilder):

    def __init__(
        self,
        cache_entries: list[CacheEntry]
    ):
        self.cache_entries = cache_entries
        self.county_ids: dict[str, Optional[int]] = self.build_county_ids_dict(cache_entries)
        self.county_municipality_ids: dict[
            str,
            dict[str, Optional[int]]
        ] = self.build_county_municipality_ids_dict(cache_entries)
        self.county_muni_entry_ids: dict[
            str,
            dict[
                str,
                dict[int, Optional[int]]
            ]
        ] = self.build_county_muni_entry_ids_dict(cache_entries)

    @staticmethod
    def build_county_ids_dict(
        entries: list[CacheEntry]
    ) -> dict[str, None]:
        return {
            county: None
            for county in
            set(
                [entry.county for entry in entries]
            )
        }

    @staticmethod
    def build_county_municipality_ids_dict(
        entries: list[CacheEntry]
    ) -> dict[str, dict[str, None]]:
        d = {}
        for entry in entries:
            # Layer 1: Counties
            if entry.county not in d:
                d[entry.county] = {}
            # Layer 2: Municipalities
            d[entry.county][entry.municipality] = None
        return d

    @staticmethod
    def build_county_muni_entry_ids_dict(
        entries: list[CacheEntry]
    ) -> dict[str, dict[str, dict[int, int]]]:
        d = {}
        for entry in entries:
            # Layer 1: Counties
            if entry.county not in d:
                d[entry.county] = {}
            # Layer 2: Municipalities
            if entry.municipality not in d[entry.county]:
                d[entry.county][entry.municipality] = {}
            # Layer 3: Years
            d[entry.county][entry.municipality][entry.year] = None
        return d

    def get_county_ids(
        self,
        session: Session,
    ) -> None:
        d = self.county_ids
        for county in d.keys():
            query = (
                select(County.id)
                .where(County.name == county)
            )
            c_id = session.execute(query).scalar_one_or_none()
            if c_id is not None:
                d[county] = c_id
                continue
            # If not in DB, add it
            county = County(name=county)
            session.add(county)
            session.flush()
            d[county.name] = county.id

    def get_county_municipality_ids(
        self,
        session: Session,
    ) -> None:
        county_ids = self.county_ids
        county_muni_ids = self.county_municipality_ids

        def muni_loop(
            county_name: str,
            muni_name: str
        ):
            county_id = county_ids[county_name]
            query = (
                select(Municipality.id)
                .where(
                    Municipality.county_id == county_id,
                    Municipality.name == muni_name
                )
            )
            m_id = session.execute(query).scalar_one_or_none()
            if m_id is not None:
                county_muni_ids[county_name][muni_name] = m_id
                return
            # If not in DB, add it
            muni_entry = Municipality(
                name=muni_name,
                county_id=county_id
            )
            session.add(muni_entry)
            session.flush()
            county_muni_ids[county_name][muni_name] = muni_entry.id

        for county in county_ids.keys():
            for municipality in county_muni_ids[county].keys():
                muni_loop(county, municipality)

    def get_county_muni_entry_ids(
        self,
        session: Session,
    ) -> None:
        county_ids = self.county_ids
        county_muni_ids = self.county_municipality_ids
        county_muni_entry_ids = self.county_muni_entry_ids

        def entry_loop(
            county_name: str,
            muni_name: str,
            year_: int
        ):
            county_id = county_ids[county_name]
            muni_id = county_muni_ids[county_name][muni_name]
            query = (
                select(AnnualReport.id)
                .where(
                    AnnualReport.county_id == county_id,
                    AnnualReport.municipality_id == muni_name,
                    AnnualReport.year == year_
                )
            )
            ar_id = session.execute(query).scalar_one_or_none()
            if ar_id is not None:
                county_muni_entry_ids[county_name][muni_name][year_] = ar_id
                return
            # If not in DB, add it
            ar_entry = AnnualReport(
                year=year_,
                county_id=county_id,
                municipality_id=muni_id
            )
            session.add(ar_entry)
            session.flush()
            county_muni_entry_ids[county_name][muni_name][year_] = ar_entry.id

        for county in county_muni_ids.keys():
            for municipality in county_muni_ids[county].keys():
                for year in county_muni_entry_ids[county][municipality].keys():
                    entry_loop(county, municipality, year)

    def get_report_id(self, entry: CacheEntry) -> int:
        county_name = entry.county_name
        muni_name = entry.municipality_name
        year = entry.year
        return self.county_muni_entry_ids[county_name][muni_name][year]

    def add_scraped(
        self,
        session: Session,
        entry: CacheEntry
    ) -> None:
        ar_id = self.get_report_id(entry)
        scraped = entry.scraped
        if not scraped:
            return
        scrape_info = ScrapeInfo(
            report_id=ar_id,
        )
        session.add(scrape_info)

    def add_scrape_error(self, session: Session, entry: CacheEntry):
        ar_id = self.get_report_id(entry)
        scraper_error = entry.scraper_error
        if scraper_error is None:
            return
        scrape_info = ScrapeError(
            report_id=ar_id,
            message=scraper_error
        )
        session.add(scrape_info)

    def add_process_error(self, session: Session, entry: CacheEntry):
        ar_id = self.get_report_id(entry)
        process_error = entry.process_error
        if process_error is None:
            return
        scrape_info = ProcessError(
            report_id=ar_id,
            message=process_error
        )
        session.add(scrape_info)

    def add_processed(
        self,
        session: Session,
        entry: CacheEntry
    ) -> None:
        ar_id = self.get_report_id(entry)
        processed = entry.processed
        if not processed:
            return
        process_info = ProcessInfo(
            report_id=ar_id,
        )
        session.add(process_info)

    def process_entry(
        self,
        session: Session,
        entry: CacheEntry
    ) -> None:
        self.add_scraped(session, entry)
        self.add_scrape_error(session, entry)
        self.add_processed(session, entry)
        self.add_process_error(session, entry)

    def run(
        self,
        session: Session,
    ) -> Any:
        self.get_county_ids(session)
        self.get_county_municipality_ids(session)
        self.get_county_muni_entry_ids(session)

        for cache_entry in self.cache_entries:
            self.process_entry(session, cache_entry)
