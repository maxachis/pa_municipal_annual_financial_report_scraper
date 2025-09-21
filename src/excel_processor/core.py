import re

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.exc import IntegrityError

from src.config import REPORT_RELEVANT_SHEET_NAME, REL_TOTAL_COLUMN, REL_CODE_COLUMN, REL_LABEL_COLUMN
from src.db.client import DatabaseClient
from src.excel_processor.constants import MAX_ROW, VALID_ROW_REGEX
from src.excel_processor.load import load_downloaded_report


class ExcelProcessor:
    """
    Class for processing scraped excel files and adding them to the database
    """

    def __init__(self):
        self.database_client = DatabaseClient()
        self.code_id_dict = self.database_client.get_code_id_dict()

    def process_downloaded_reports(self):
        unprocessed_downloaded_reports = self.database_client.get_unprocessed_downloaded_reports()

        for report in unprocessed_downloaded_reports:
            print(f"Processing {report.report_id}: {report.xlsx_file}")
            wb = load_downloaded_report(report.xlsx_file)
            self.process_downloaded_report(wb, report.report_id)
            self.database_client.mark_as_processed(report.report_id)

    def process_downloaded_report(self, wb: Workbook, report_id: int):
        # Get sheet
        ws: Worksheet = wb[REPORT_RELEVANT_SHEET_NAME]

        # Iterate through rows until getting to end
        for row in ws.iter_rows(
                min_row=1,
                max_row=MAX_ROW,
                min_col=1,
                max_col=REL_TOTAL_COLUMN,
                values_only=True
        ):
            if row[0] is None:
                continue
            if not re.match(VALID_ROW_REGEX, row[0]):
                continue
            code = row[REL_CODE_COLUMN - 1]
            label = row[REL_LABEL_COLUMN - 1]
            total = row[REL_TOTAL_COLUMN - 1]
            if not self.database_client.code_label_exists(code):
                self.database_client.add_code_label(code, label)
            try:
                code_id = self.code_id_dict[code]
                self.database_client.add_to_annual_financial_report_details_table(
                    report_id=report_id,
                    code_id=code_id,
                    total=total
                )
            except IntegrityError:
                pass

