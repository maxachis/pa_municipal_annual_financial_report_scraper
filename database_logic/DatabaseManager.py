from functools import wraps
from typing import Optional

from sqlalchemy import create_engine, select, case, func
from sqlalchemy.orm import sessionmaker, Session

from config import FEDERAL_CODES, STATE_CODES, LOCAL_CODES
from database_logic.models import Base, AnnualFinancialReportDetails, Code
from report_creator.data_objects import CMYBreakdownRow


class DatabaseManager:
    """
    The database manager is the primary interface for the SQLite database.
    It utilizes SQLAlchemy to interact with the database.
    """
    def __init__(self):
        self.engine = create_engine('sqlite:///database.db')
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
                            AnnualFinancialReportDetails.code.in_(
                                FEDERAL_CODES
                            ),
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0)
                ).label("federal_amt"),
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.in_(
                                STATE_CODES
                            ),
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0
                    )
                ).label("state_amt"),
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.in_(
                                LOCAL_CODES
                            ),
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

