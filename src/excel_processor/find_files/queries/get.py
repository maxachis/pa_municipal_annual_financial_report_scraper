from typing import Any, Sequence

from sqlalchemy import select, RowMapping
from sqlalchemy.orm import Session

from src.db.models.sqlalchemy.impl import ScrapeInfo, AnnualReport, Municipality, County
from src.db.queries.base import QueryBuilder
from src.excel_processor.find_files.models.input_ import FindFilesInput


class GetReportsMissingFilesQuery(QueryBuilder):

    def run(self, session: Session) -> list[FindFilesInput]:
        query = (
            select(
                ScrapeInfo.id.label("scrape_info_id"),
                Municipality.name.label("municipality_name"),
                County.name.label("county_name"),
                AnnualReport.year,
            )
            .join(
                AnnualReport,
                AnnualReport.id == ScrapeInfo.report_id,
            )
            .join(
                Municipality,
                Municipality.id == AnnualReport.municipality_id,
            )
            .join(
                County,
                County.id == AnnualReport.county_id,
            )
            .where(
                ScrapeInfo.filename.is_(None)
            )
        )

        mappings: Sequence[RowMapping] = session.execute(query).mappings().all()

        return [
            FindFilesInput(**mapping) for mapping in mappings
        ]
