from functools import wraps
from typing import Optional

from sqlalchemy import create_engine, select, case, func, or_
from sqlalchemy.orm import sessionmaker, Session

from config import FEDERAL_CODES, STATE_CODES, LOCAL_CODES, FEDERAL_PREFIX, STATE_PREFIX, LOCAL_PREFIX
from db.models.pydantic.cache_entry import CacheEntry
from db.models.pydantic.pop_row import PopRow
from db.models.sqlalchemy.instantiations import CodeV2, AnnualReport, ReportDetails, County, Municipality
from db.queries.instantiations.add_pop_rows import AddPopRowsQueryBuilder
from db.queries.instantiations.convert_state_to_db import ConvertStateToDBQueryBuilder
from report_creator.data_objects import CMYBreakdownRow, AverageRow, AverageWithPopRow


class DatabaseClient:
    """
    The database client is the primary interface for the SQLite database.
    It utilizes SQLAlchemy to interact with the database.
    """

    def __init__(self):
        self.engine = create_engine("postgresql://myuser:mypass@host.docker.internal/mydb")
        self.session_maker = sessionmaker(bind=self.engine, expire_on_commit=False)

    @staticmethod
    def session_manager(method):
        """Decorator to manage async session lifecycle."""

        @wraps(method)
        def wrapper(self, *args, **kwargs):
            with self.session_maker() as session:
                with session.begin():
                    try:
                        result = method(self, session, *args, **kwargs)
                        return result
                    except Exception as e:
                        session.rollback()
                        raise e

        return wrapper

    @session_manager
    def code_label_exists(self, session: Session, code: str) -> bool:
        code_label = session.query(CodeV2).filter_by(code=code).first()
        return code_label is not None

    @session_manager
    def add_code_label(self, session: Session, code: str, label: str):
        code_label = CodeV2(code=code, label=label)
        session.add(code_label)

    @session_manager
    def add_to_annual_financial_report_details_table(
        self,
        session: Session,
        county: str,
        municipality: str,
        year: str,
        code: str,
        total: Optional[int]
    ):
        raise NotImplementedError

    @session_manager
    def get_row_breakdowns(self, session: Session) -> list[CMYBreakdownRow]:
        federal_amt_label = "federal_amt"
        state_amt_label = "state_amt"
        local_amt_label = "local_amt"

        def helper(when):
            return func.sum(
                case(
                    (
                        when,
                        ReportDetails.total
                    ),
                    else_=0
                )
            )


        cte = (
            select(
                ReportDetails.report_id,
                helper(
                    CodeV2.code.like(f"{FEDERAL_PREFIX}%")
                ).label(federal_amt_label),
                helper(
                    or_(
                        CodeV2.code.in_(
                            STATE_CODES
                        ),
                        CodeV2.code.like(f"{STATE_PREFIX}%")
                    )
                ).label(state_amt_label),
                helper(
                    CodeV2.code.like(f"{LOCAL_PREFIX}%"),
                ).label(local_amt_label)
            )
            .group_by(
                ReportDetails.id
            ).cte()
        )
        c = cte.c

        query = (
            select(
                County.name,
                Municipality.name,
                AnnualReport.year,
                c[federal_amt_label].label(federal_amt_label),
                c[state_amt_label].label(state_amt_label),
                c[local_amt_label].label(local_amt_label)
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
        )

        all_results = session.execute(query).mappings().all()

        return [CMYBreakdownRow(**result) for result in all_results]

    @session_manager
    def get_county_municipality_averages(
        self,
        session: Session
    ) -> list[AverageRow]:

        sum_federal_label = "sum_federal"
        sum_state_label = "sum_state"
        sum_local_label = "sum_local"

        stmt = (
            select(
                ReportDetails.report_id,
                func.sum(
                    case(
                        (
                            CodeV2.code.in_(
                                FEDERAL_CODES
                            ), ReportDetails.total),
                        else_=0
                    )
                ).label(sum_federal_label),
                func.sum(
                    case(
                        (
                            CodeV2.code.in_(
                                STATE_CODES
                            ), ReportDetails.total),
                        else_=0
                    )
                ).label(sum_state_label),
                func.sum(
                    case(
                        (
                            CodeV2.code.in_(
                                LOCAL_CODES
                            ), ReportDetails.total),
                        else_=0
                    )
                ).label(sum_local_label),
            )
            .group_by(
                ReportDetails.report_id
            )
            .cte()
        )
        c = stmt.c
        sum_federal_amt = c[sum_federal_label]
        sum_state_amt = c[sum_state_label]
        sum_local_amt = c[sum_local_label]

        final_query = (
            select(
                County.name,
                Municipality.name,
                func.avg(sum_federal_amt).label("federal_average"),
                func.avg(sum_state_amt).label("state_average"),
                func.avg(sum_local_amt).label("local_average"),
            )
            .join(AnnualReport, AnnualReport.id == c.report_id)
            .join(County, County.id == c.county_id)
            .join(Municipality, Municipality.id == c.municipality_id)
            .group_by(
                County.name,
                Municipality.name
            )
        )

        all_results = session.execute(final_query).mappings().all()

        return [AverageRow(**result) for result in all_results]

    @session_manager
    def wipe_table(self, session: Session, model) -> None:
        session.query(model).delete()

    @session_manager
    def get_average_with_pop_rows(self, session: Session) -> list[AverageWithPopRow]:
        raise NotImplementedError

    @session_manager
    def convert_state_to_db(
        self,
        session: Session,
        entries: list[CacheEntry]
    ) -> None:
        query_builder = ConvertStateToDBQueryBuilder(entries)
        query_builder.run(session)

    @session_manager
    def add_pop_rows(
        self,
        session: Session,
        pop_rows: list[PopRow]
    ) -> None:
        query_builder = AddPopRowsQueryBuilder(pop_rows)
        query_builder.run(session)