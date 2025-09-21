from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.models.sqlalchemy.impl import ScrapeInfo
from src.db.queries.base import QueryBuilder
from src.excel_processor.find_files.models.insert import ReportFileInsert


class InsertReportFileQueryBuilder(QueryBuilder):

    def __init__(self, report_file: ReportFileInsert):
        self.report_file = report_file

    def run(self, session: Session) -> None:
        statement = (
            update(ScrapeInfo)
            .where(
                ScrapeInfo.report_id == self.report_file.report_id
            )
            .values(
                filename=self.report_file.file_name
            )
        )
        try:
            session.execute(statement)
            session.commit()
        except IntegrityError:
            print(f"Integrity error for report_id: {self.report_file.report_id}")
            session.rollback()
