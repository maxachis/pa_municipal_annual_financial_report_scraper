from functools import wraps
from typing import Optional

from sqlalchemy import create_engine, select, case, func, or_, Float, cast
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker, Session

from src.config import FEDERAL_CODES, STATE_CODES, LOCAL_CODES, FEDERAL_PREFIX, STATE_PREFIX, LOCAL_PREFIX, YEARS
from src.db.models.pydantic.pop_row import PopRow
from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.impl import CodeV2, AnnualReport, ReportDetails, County, Municipality, \
    ScrapeInfo, \
    ScrapeError, ProcessInfo, JoinedPopDetailsV2
from src.db.queries.instantiations.add_pop_rows import AddPopRowsQueryBuilder
from src.db.queries.instantiations.get_average_with_pop_rows import GetAverageWithPopRowsQueryBuilder
from src.db.queries.instantiations.get_row_breakdowns import GetRowBreakdownsQueryBuilder
from src.excel_processor.models.downloaded_report import DownloadedReportMetadata
from src.report_creator.models.average_with_pop import AverageWithPopRow
from src.report_creator.models.cmy_breakdown import CMYBreakdownRow
from src.scraper.models.name_id import NameID


class DatabaseClient:
    """
    The database client is the primary interface for the SQLite database.
    It utilizes SQLAlchemy to interact with the database.
    """

    def __init__(self):
        self.engine = create_engine("postgresql://myuser:mypass@host.docker.internal/mydb")
        self.session_maker = sessionmaker(
            bind=self.engine,
            expire_on_commit=False
        )

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
    def add_all(
        self,
        session: Session,
        models: list[Base],
        return_ids: bool = False
    ) -> list[int] | None:
        session.add_all(models)
        session.flush()
        if return_ids:
            return [model.id for model in models]
        return None

    @session_manager
    def add_to_annual_financial_report_details_table(
        self,
        session: Session,
        report_id: int,
        code_id: int,
        total: Optional[int]
    ):
        details = ReportDetails(
            report_id=report_id,
            code_id=code_id,
            total=total
        )
        session.add(details)

    @session_manager
    def get_unprocessed_downloaded_reports(
        self,
        session: Session
    ) -> list[DownloadedReportMetadata]:
        query = (
            select(
                ScrapeInfo.report_id,
                ScrapeInfo.filename.label("xlsx_file")
            )
            .where(
                ScrapeInfo.filename.is_not(None)
            )
        )

        all_results = session.execute(query).mappings().all()

        return [DownloadedReportMetadata(**result) for result in all_results]

    @session_manager
    def get_row_breakdowns(self, session: Session) -> list[CMYBreakdownRow]:
        builder = GetRowBreakdownsQueryBuilder()
        return builder.run(session)

    @session_manager
    def wipe_table(self, session: Session, model) -> None:
        session.query(model).delete()

    @session_manager
    def get_average_with_pop_rows(self, session: Session) -> list[AverageWithPopRow]:
        builder = GetAverageWithPopRowsQueryBuilder()
        return builder.run(session)

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
            # Only allow one error per report
            return


    @session_manager
    def mark_as_scraped(self, session: Session, report_id, filename: Optional[str] = None):
        scrape_info = ScrapeInfo(
            report_id=report_id,
            filename=filename
        )
        session.add(scrape_info)

    @session_manager
    def mark_as_processed(self, session: Session, report_id: int):
        process_info = ProcessInfo(report_id=report_id)
        session.add(process_info)

    @session_manager
    def has_timeout_error(self, session: Session, report_id: int) -> bool:
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
        return len(results) >= len(YEARS)

    @session_manager
    def get_code_id_dict(self, session: Session) -> dict[str, int]:
        query = (
            select(
                CodeV2.code,
                CodeV2.id
            )
        )
        result = session.execute(query).all()
        return {code: id for code, id in result}
