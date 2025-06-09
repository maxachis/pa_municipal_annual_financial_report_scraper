from functools import wraps
from typing import Optional

from sqlalchemy import create_engine, select, case, func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from config import FEDERAL_CODES, STATE_CODES, LOCAL_CODES, FEDERAL_PREFIX, STATE_PREFIX, LOCAL_PREFIX, YEARS
from db.models.pydantic.pop_row import PopRow
from db.models.sqlalchemy.instantiations import CodeV2, AnnualReport, ReportDetails, County, Municipality, ScrapeInfo, \
    ScrapeError
from db.queries.instantiations.add_pop_rows import AddPopRowsQueryBuilder
from report_creator.models.average_with_pop import AverageWithPopRow
from report_creator.models.average import AverageRow
from report_creator.models.cmy_breakdown import CMYBreakdownRow
from scraper.models.name_id import NameID


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
    def add_pop_rows(
        self,
        session: Session,
        pop_rows: list[PopRow]
    ) -> None:
        query_builder = AddPopRowsQueryBuilder(pop_rows)
        query_builder.run(session)

    @session_manager
    def get_county_info(self, session: Session, label: str) -> NameID:
        """
        Get county id for county, or create county if it doesn't exist
        :param session:
        :param label:
        :return:
        """
        query = (
            select(County)
            .filter(County.name == label)
        )
        county = session.execute(query).scalars().one_or_none()
        if county is None:
            county = County(name=label)
            session.add(county)
            session.flush()
        return NameID(
            id=county.id,
            name=county.name
        )

    @session_manager
    def get_municipality_info(
        self,
        session: Session,
        county_id: int,
        label: str
    ) -> NameID:
        query = (
            select(Municipality)
            .filter(Municipality.name == label)
            .filter(Municipality.county_id == county_id)
        )
        muni = session.execute(query).scalars().one_or_none()
        if muni is None:
            muni = Municipality(name=label, county_id=county_id)
            session.add(muni)
            session.flush()
        return NameID(
            id=muni.id,
            name=muni.name
        )

    @session_manager
    def get_report_id(
        self,
        session: Session,
        county_id: int,
        muni_id: int,
        year: int
    ) -> NameID:
        query = (
            select(AnnualReport)
            .filter(AnnualReport.county_id == county_id)
            .filter(AnnualReport.municipality_id == muni_id)
            .filter(AnnualReport.year == year)
        )
        report = session.execute(query).scalars().one_or_none()
        if report is None:
            report = AnnualReport(county_id=county_id, municipality_id=muni_id, year=year)
            session.add(report)
            session.flush()
        return NameID(
            id=report.id,
            name=f"{report.county.name} {report.municipality.name} {report.year}"
        )

    @session_manager
    def is_scraped(self, session: Session, report_id: int) -> bool:
        query = select(
            ScrapeInfo
        ).where(
            ScrapeInfo.report_id == report_id
        )

        result = session.execute(query).scalars().one_or_none()
        return result is not None

    @session_manager
    def add_scraper_error(
        self,
        session: Session,
        report_id: int,
        error: str,
    ):
        scrape_info = ScrapeError(report_id=report_id, message=error)
        try:
            session.add(scrape_info)
            session.flush()
        except IntegrityError:
            query = (
                select(ScrapeError)
                .filter(ScrapeError.report_id == report_id)
            )
            result = session.execute(query).scalars().one_or_none()
            result.message = error

    @session_manager
    def mark_as_scraped(self, session: Session, report_id, filename: Optional[str] = None):
        scrape_info = ScrapeInfo(
            report_id=report_id,
            filename=filename
        )
        session.add(scrape_info)

    @session_manager
    def has_timeout_error(self, session: Session, report_id):
        query = (
            select(ScrapeError)
            .filter(ScrapeError.report_id == report_id)
            .filter(ScrapeError.message.contains("Timeout"))
        )
        result = session.execute(query).scalars().one_or_none()
        return result is not None

    @session_manager
    def all_years_scraped(
        self,
        session: Session,
        county_id: int,
        muni_id: int
    ):
        query = (
            select(AnnualReport)
            .where(
                AnnualReport.county_id == county_id,
                AnnualReport.municipality_id == muni_id,
                ScrapeInfo.id != None
            )
            .outerjoin(
                ScrapeInfo,
            )
        )
        results = session.execute(query).scalars().all()
        return len(results) == len(YEARS)
