from typing import Any

from sqlalchemy import func, case, select, or_
from sqlalchemy.orm import Session

from src.config import FEDERAL_PREFIX, STATE_CODES, STATE_PREFIX, LOCAL_PREFIX
from src.db.models.sqlalchemy.impl import ReportDetails, CodeV2, County, Municipality, AnnualReport
from src.db.queries.base import QueryBuilder
from src.db.queries.helpers import get_federal_conditions, get_state_conditions, get_local_conditions
from src.report_creator.models.cmy_breakdown import CMYBreakdownRow


class GetRowBreakdownsQueryBuilder(QueryBuilder):

    def __init__(self):
        self.federal_amt_label = "federal_amt"
        self.state_amt_label = "state_amt"
        self.local_amt_label = "local_amt"

    def helper(self, when):
        return func.sum(
            case(
                (
                    when,
                    ReportDetails.total
                ),
                else_=0
            )
        )

    def run(self, session: Session) -> list[CMYBreakdownRow]:
        cte = (
            select(
                ReportDetails.report_id,
                self.helper(
                    get_federal_conditions()
                ).label(self.federal_amt_label),
                self.helper(
                    get_state_conditions()
                ).label(self.state_amt_label),
                self.helper(
                    get_local_conditions()
                ).label(self.local_amt_label)
            )
            .join(
                CodeV2,
                CodeV2.id == ReportDetails.code_id
            )
            .group_by(
                ReportDetails.report_id
            ).cte()
        )
        c = cte.c

        query = (
            select(
                County.name.label("county"),
                Municipality.name.label("municipality"),
                AnnualReport.year.label("year"),
                c[self.federal_amt_label].label(self.federal_amt_label),
                c[self.state_amt_label].label(self.state_amt_label),
                c[self.local_amt_label].label(self.local_amt_label)
            )
            .join(
                AnnualReport,
                AnnualReport.id == c.report_id
            )
            .join(
                County,
                County.id == AnnualReport.county_id
            )
            .join(
                Municipality,
                Municipality.id == AnnualReport.municipality_id
            )
            .order_by(
                County.name,
                Municipality.name,
                AnnualReport.year
            )
        )

        all_results = session.execute(query).mappings().all()

        return [
            CMYBreakdownRow(
                **result
            )
            for result in all_results]
