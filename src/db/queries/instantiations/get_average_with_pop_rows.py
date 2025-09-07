from sqlalchemy import select, cast, func, case, Float, Cast, distinct
from sqlalchemy.orm import Session

from src.db.models.sqlalchemy.instantiations import AnnualReport, CodeV2, ReportDetails, County, Municipality, \
    JoinedPopDetailsV2
from src.db.queries.base import QueryBuilder
from src.db.queries.helpers import get_state_conditions, get_federal_conditions, get_local_conditions
from src.report_creator.models.average_with_pop import AverageWithPopRow


class GetAverageWithPopRowsQueryBuilder(QueryBuilder):

    def __init__(self):
        self.avg_federal_label = "avg_federal"
        self.avg_state_label = "avg_state"
        self.avg_local_label = "avg_local"

    @staticmethod
    def case_sum(when) -> Cast:
        return cast(
            func.sum(
                case(
                    (when, ReportDetails.total),
                    else_ = 0
                ),
            ) / func.count(distinct(AnnualReport.year)), Float
        )

    def run(self, session: Session) -> list[AverageWithPopRow]:
        stmt = (
            select(
                AnnualReport.municipality_id,
                self.case_sum(
                    get_federal_conditions()
                ).label(self.avg_federal_label),
                self.case_sum(
                    get_state_conditions()
                ).label(self.avg_state_label),
                self.case_sum(
                    get_local_conditions(),
                ).label(self.avg_local_label),
            )
            .select_from(
                AnnualReport
            )
            .join(
                ReportDetails,
                ReportDetails.report_id == AnnualReport.id
            )
            .join(
                CodeV2,
                CodeV2.id == ReportDetails.code_id
            )
            .group_by(
                AnnualReport.municipality_id
            )
            .cte()
        )
        c = stmt.c
        avg_federal_amt = c[self.avg_federal_label]
        avg_state_amt = c[self.avg_state_label]
        avg_local_amt = c[self.avg_local_label]
        query = (
            select(
                County.name.label("county"),
                Municipality.name.label("municipality"),
                JoinedPopDetailsV2.class_.label("class_"),
                JoinedPopDetailsV2.location_type.label("urban_rural"),
                JoinedPopDetailsV2.pop_estimate.label("pop_estimate"),
                JoinedPopDetailsV2.pop_margin.label("pop_margin"),
                avg_federal_amt.label("federal_average"),
                avg_state_amt.label("state_average"),
                avg_local_amt.label("local_average"),
            )
            .select_from(
                Municipality
            )
            .join(
                County,
                County.id == Municipality.county_id
            )
            .join(
                JoinedPopDetailsV2,
                JoinedPopDetailsV2.municipality_id == Municipality.id
            )
            .join(
                stmt,
                stmt.c.municipality_id == JoinedPopDetailsV2.municipality_id
            )
            .order_by(
                County.name,
                Municipality.name
            )
        )

        results = session.execute(query).mappings().all()

        return [
            AverageWithPopRow(
                **result
            )
            for result in results
        ]
