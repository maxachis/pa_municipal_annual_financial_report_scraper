from functools import wraps
from typing import Optional

from sqlalchemy import create_engine, select, case, func
from sqlalchemy.orm import sessionmaker, Session

from database_logic.models import Base, AnnualFinancialReportDetails, CodeLabel
from report_creator.data_objects import CMYBreakdownRow


class DatabaseManager:
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
        code_label = session.query(CodeLabel).filter_by(code=code).first()
        return code_label is not None



    @session_manager
    def add_code_label(self, session: Session, code: str, label: str):
        code_label = CodeLabel(code=code, label=label)
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
        # Define your sets
        federal_codes = [
            '351.01',
            '351.02',
            '351.03',
            '351.04',
            '351.05',
            '351.06',
            '351.07',
            '351.08',
            '351.09',
            '351.1',
            '351.11',
            '351.12',
            '351.13',
            '351.XX'
        ]
        state_codes = [
            '354.01',
            '354.02',
            '354.03',
            '354.04',
            '345.05',
            '345.06',
            '345.07',
            '345.08',
            '354.09',
            '354.1',
            '354.11',
            '354.12',
            '354.13',
            '354.14',
            '354.15',
            '354.XX',
            '355.08'
        ]
        local_codes = [
            '357.01',
            '357.02',
            '357.03',
            '357.XX'
        ]


        query = (
            select(
                AnnualFinancialReportDetails.county,
                AnnualFinancialReportDetails.municipality,
                AnnualFinancialReportDetails.year,
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.in_(
                                federal_codes
                            ),
                            AnnualFinancialReportDetails.total
                        ),
                        else_=0)
                ).label("federal_amt"),
                func.sum(
                    case(
                        (
                            AnnualFinancialReportDetails.code.in_(
                                state_codes
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
                                local_codes
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

