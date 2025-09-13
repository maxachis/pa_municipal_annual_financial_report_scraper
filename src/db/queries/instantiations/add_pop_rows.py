from rapidfuzz.fuzz import ratio
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models.pydantic.pop_row import PopRow
from src.db.models.sqlalchemy.impl import County, Municipality, JoinedPopDetailsV2
from src.db.queries.base import QueryBuilder


class AddPopRowsQueryBuilder(QueryBuilder):

    def __init__(
        self,
        pop_rows: list[PopRow]
    ):
        self.pop_rows = pop_rows
        self.county_ids: dict[str, int] = {}
        self.county_muni_ids: dict[int, dict[str, int]] = {}

    def get_county_ids(self, session: Session) -> None:
        query = (
            select(County)
        )
        counties = session.execute(query).scalars().all()
        for county in counties:
            self.county_ids[county.name] = county.id

    def get_county_muni_ids(self, session: Session) -> None:
        query = (
            select(
                Municipality
            )
        )
        munis = session.execute(query).scalars().all()
        for muni in munis:
            if muni.county_id not in self.county_muni_ids:
                self.county_muni_ids[muni.county_id] = {}
            self.county_muni_ids[muni.county_id][muni.name] = muni.id


    def get_best_county_match(self, county: str) -> int:
        all_counties = self.county_ids.keys()

        def score(county_name: str) -> float:
            return ratio(county_name.lower(), county.lower())

        best_county = max(all_counties, key=score)
        best_county_id = self.county_ids[best_county]
        return best_county_id

    def get_best_muni_match(self, county_id: int, municipality: str) -> int:
        all_munis = self.county_muni_ids[county_id].keys()

        def score(muni_name: str) -> float:
            return ratio(muni_name.lower(), municipality.lower())

        best_muni = max(all_munis, key=score)
        best_muni_id = self.county_muni_ids[county_id][best_muni]
        return best_muni_id

    def run(self, session: Session) -> None:

        self.get_county_ids(session)
        self.get_county_muni_ids(session)
        for pop_row in self.pop_rows:

            # Get id for best county match
            best_county_id = self.get_best_county_match(pop_row.county)

            # Get id for best municipality match, given county
            best_muni_id = self.get_best_muni_match(best_county_id, pop_row.municipality)

            obj = JoinedPopDetailsV2(
                geo_id=pop_row.geo_id,
                county_id=best_county_id,
                municipality_id=best_muni_id,
                class_=pop_row.class_,
                pop_estimate=pop_row.pop_estimate,
                pop_margin=pop_row.pop_margin,
                location_type=pop_row.location_type.value
            )
            session.add(obj)
            session.flush()

