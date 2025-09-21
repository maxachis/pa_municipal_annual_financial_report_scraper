from typing import Sequence

from sqlalchemy import select, exists, RowMapping
from sqlalchemy.orm import Session

from src.db.models.sqlalchemy.impl import ScrapeInfo
from src.db.models.sqlalchemy.impl.total_revenue import TotalRevenue
from src.db.queries.base import QueryBuilder
from src.excel_processor.total_revenue.models.file_report_mapping import FileReportMapping


class GetReportsMissingTotalRevenueQueryBuilder(QueryBuilder):

    def run(self, session: Session) -> list[FileReportMapping]:
        statement = (
            select(
                ScrapeInfo.report_id,
                ScrapeInfo.filename,
            )
            .where(
                ~exists(
                    TotalRevenue.id
                ).where(
                    TotalRevenue.report_id == ScrapeInfo.report_id
                ),
                ScrapeInfo.filename.isnot(None)
            )
        )

        mappings: Sequence[RowMapping] = session.execute(statement).mappings().all()

        return [
            FileReportMapping(**mapping) for mapping in mappings
        ]


