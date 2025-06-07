from functools import wraps
from typing import Optional

from rapidfuzz.fuzz import ratio
from sqlalchemy import create_engine, select, case, func, Select, or_
from sqlalchemy.orm import sessionmaker, Session

from config import FEDERAL_CODES, STATE_CODES, LOCAL_CODES, FEDERAL_PREFIX, STATE_PREFIX, LOCAL_PREFIX
from db.models.pydantic import PopRow
from db.models.sqlalchemy import Base, AnnualFinancialReportDetails, Code, JoinedPopDetails, IntermediateTable
from report_creator.data_objects import CMYBreakdownRow, AverageRow, AverageWithPopRow
from util import project_path


class DatabaseManager:
    """
    The database manager is the primary interface for the SQLite database.
    It utilizes SQLAlchemy to interact with the database.
    """
    def __init__(self):
        path = project_path("database.db")
        self.engine = create_engine(f"sqlite:///{path}")
        Base.metadata.create_all(self.engine)
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
        code_label = session.query(Code).filter_by(code=code).first()
        return code_label is not None



    @session_manager
    def add_code_label(self, session: Session, code: str, label: str):
        code_label = Code(code=code, label=label)
        session.add(code_label)

    @session_manager
    def add_pop_row(
            self,
            session: Session,
            geo_id: str,
            county: str,
            municipality: str,
            class_: str,
            pop_estimate: int,
            pop_margin: int,
            urban_rural: str
    ):
        pop_row = JoinedPopDetails(
            geo_id=geo_id,
            county=county,
            municipality=municipality,
            class_=class_,
            pop_estimate=pop_estimate,
            pop_margin=pop_margin,
            urban_rural=urban_rural
        )
        session.add(pop_row)

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
        details = AnnualFinancialReportDetails(
            county=county,
            municipality=municipality,
            year=year,
            code=code,
            total=total
        )
        session.add(details)

    @session_manager
    def get_row_breakdowns(self, session: Session) -> list[CMYBreakdownRow]:
        query = (
            select(
                AnnualFinancialReportDetails.county,
                AnnualFinancialReportDetails.municipality,
                AnnualFinancialReportDetails.year,
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.like(f"{FEDERAL_PREFIX}%"),
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0)
                ).label("federal_amt"),
                func.sum(
                    case(
                        (
                            or_(
                                AnnualFinancialReportDetails.code.in_(
                                    STATE_CODES
                                ),
                                AnnualFinancialReportDetails.code.like(f"{STATE_PREFIX}%")
                            )
                            ,
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0
                    )
                ).label("state_amt"),
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.like(f"{LOCAL_PREFIX}%"),
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0
                    )
                ).label("local_amt"),
            )
            .group_by(
                AnnualFinancialReportDetails.county,
                AnnualFinancialReportDetails.municipality,
                AnnualFinancialReportDetails.year
            )
        )

        all_results = session.execute(query).mappings().all()

        return [CMYBreakdownRow(**result) for result in all_results]


    @session_manager
    def get_county_municipality_averages(
            self,
            session: Session
    ) -> list[AverageRow]:

        stmt = (
            select(
                AnnualFinancialReportDetails.county,
                AnnualFinancialReportDetails.municipality,
                AnnualFinancialReportDetails.year,
                        func.sum(
                            case(
                                (
                                    AnnualFinancialReportDetails.code.in_(
                                        FEDERAL_CODES
                                    ), AnnualFinancialReportDetails.total),
                                    else_=0
                            )
                        ).label("sum_federal"),
                        func.sum(
                            case(
                                (
                                    AnnualFinancialReportDetails.code.in_(
                                        STATE_CODES
                                    ), AnnualFinancialReportDetails.total),
                                    else_=0
                            )
                        ).label("sum_state"),
                        func.sum(
                            case(
                                (
                                    AnnualFinancialReportDetails.code.in_(
                                        LOCAL_CODES
                                    ), AnnualFinancialReportDetails.total),
                                    else_=0
                            )
                        ).label("sum_local"),
            )
            .group_by(
                AnnualFinancialReportDetails.county,
                AnnualFinancialReportDetails.municipality,
                AnnualFinancialReportDetails.year
            )
            .subquery()
        )

        final_query = (
            select(
                stmt.c.county,
                stmt.c.municipality,
                func.avg(stmt.c.sum_federal).label("federal_average"),
                func.avg(stmt.c.sum_state).label("state_average"),
                func.avg(stmt.c.sum_local).label("local_average"),
            )
            .group_by(stmt.c.county, stmt.c.municipality)
        )

        all_results = session.execute(final_query).mappings().all()

        return [AverageRow(**result) for result in all_results]

    def get_best_fuzzy_match(
            self,
            session: Session,
            county: str,
            municipality: str
    ) -> PopRow:
        # Fetch all rows from the table
        result = session.execute(select(JoinedPopDetails))
        rows = result.scalars().all()

        # Define a scoring function using rapidfuzz
        def score(row: JoinedPopDetails):
            return (
                    ratio(row.county, county) +
                    ratio(row.municipality, municipality)
            )

        # Get the row with the highest combined score
        best_row = max(rows, key=score)
        return PopRow(
            geo_id=best_row.geo_id,
            county=best_row.county,
            municipality=best_row.municipality,
            class_=best_row.class_,
            pop_estimate=best_row.pop_estimate,
            pop_margin=best_row.pop_margin,
            urban_rural=best_row.urban_rural
        )

    @session_manager
    def wipe_table(self, session: Session, model) -> None:
        session.query(model).delete()

    @session_manager
    def get_average_with_pop_rows(self, session: Session) -> list[AverageWithPopRow]:
        query = Select(IntermediateTable)
        results = session.execute(query).scalars().all()
        final_results = []
        for result in results:
            row = AverageWithPopRow(
                county=result.county_downloaded,
                municipality=result.municipality_downloaded,
                federal_average=result.federal_average,
                state_average=result.state_average,
                local_average=result.local_average,
                pop_estimate=result.pop_estimate,
                pop_margin=result.pop_margin,
                urban_rural=result.urban_rural,
                class_=result.class_
            )
            final_results.append(row)

        return final_results


    @session_manager
    def build_intermediate_table(self, session: Session) -> None:
        """
        Build an intermediate table based on fuzzy string matching
        First by finding the county that is the best match
        Then by finding the best municipality within that county
        :param session:
        :return:
        """


        average_rows = self.get_county_municipality_averages()

        for average_row in average_rows:
            # First, get best county match
            county = average_row.county
            municipality = average_row.municipality
            def score_county(row: JoinedPopDetails):
                return ratio(row.county.strip().upper(), county.strip().upper())

            def score_municipality(row: JoinedPopDetails):
                return ratio(row.municipality.strip().upper(), municipality.strip().upper())

            result = session.execute(select(JoinedPopDetails))
            rows = result.scalars().all()

            best_county_row = max(rows, key=score_county)

            # Then, get best municipality match
            result = session.execute(
                select(JoinedPopDetails).
                where(JoinedPopDetails.county == best_county_row.county)
            )
            rows = result.scalars().all()

            pop_row = max(rows, key=score_municipality)


            session.add(
                IntermediateTable(
                   geo_id=pop_row.geo_id,
                    county_downloaded=average_row.county,
                    municipality_downloaded=average_row.municipality,
                    county_joined=pop_row.county,
                    municipality_joined=pop_row.municipality,
                    class_=pop_row.class_,
                    pop_estimate=pop_row.pop_estimate,
                    pop_margin=pop_row.pop_margin,
                    urban_rural=pop_row.urban_rural,
                    federal_average=average_row.federal_average,
                    state_average=average_row.state_average,
                    local_average=average_row.local_average
                )
            )
