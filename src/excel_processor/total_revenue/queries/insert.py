from typing import Any

from sqlalchemy.orm import Session

from src.db.models.sqlalchemy.impl.total_revenue import TotalRevenue
from src.db.queries.base import QueryBuilder


class InsertTotalRevenueQueryBuilder(QueryBuilder):

    def __init__(self, report_id: int, total_revenue: int):
        self.report_id = report_id
        self.total_revenue = total_revenue

    def run(self, session: Session) -> Any:
        insert_model = TotalRevenue(
            report_id=self.report_id,
            total=self.total_revenue
        )
        session.add(insert_model)
