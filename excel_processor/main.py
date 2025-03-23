import re

from openpyxl.reader.excel import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.exc import IntegrityError

from config import SHEET_NAME, TOTAL_COLUMN, CODE_COLUMN, LABEL_COLUMN
from database_logic.DatabaseManager import DatabaseManager
from scraper.JsonCache import JsonCache
from scraper.data_objects import CMY

MAX_ROW = 1000
VALID_ROW_REGEX = r"^[\d\-\.]+$"  # Regex for row containing only numbers, decimals, and hyphens

def open_excel_file(file_path: str) -> Workbook:
    return load_workbook(file_path)

class ExcelProcessor:
    """
    Class for processing scraped excel files and adding them to the database
    """

    def __init__(self):
        self.database_manager = DatabaseManager()
        self.cache = JsonCache("cache.json")
        self.cache.load_cache()

    def process(self):
        for cmy in self.cache.get_as_list_of_CMY():
            print(f"Processing {cmy.county} {cmy.municipality} {cmy.year}")
            try:
                wb = self.get_excel_file(cmy)
                self.process_excel_file(wb, cmy)
                self.cache.mark_as_processed(cmy)
            except Exception as e:
                print(f"Error processing {cmy.county} {cmy.municipality} {cmy.year}: {e}")
                self.cache.add_process_error(cmy, str(e))

    def get_excel_file(self, cmy: CMY) -> Workbook:
        return open_excel_file(f"downloads/report_{cmy.county}_{cmy.municipality}_{cmy.year}.xlsx")

    def process_excel_file(self, wb: Workbook, cmy: CMY):
        # Get sheet
        ws: Worksheet = wb[SHEET_NAME]

        # Iterate through rows until getting to end
        for row in ws.iter_rows(
                min_row=1,
                max_row=MAX_ROW,
                min_col=1,
                max_col=TOTAL_COLUMN,
                values_only=True
        ):
            if row[0] is None:
                continue
            if not re.match(VALID_ROW_REGEX, row[0]):
                continue
            code = row[CODE_COLUMN-1]
            label = row[LABEL_COLUMN-1]
            total = row[TOTAL_COLUMN-1]
            if not self.database_manager.code_label_exists(code):
                self.database_manager.add_code_label(code, label)
            try:
                self.database_manager.add_to_annual_financial_report_details_table(
                    county=cmy.county,
                    municipality=cmy.municipality,
                    year=cmy.year,
                    code=code,
                    total=total
                )
            except IntegrityError:
                pass







if __name__ == "__main__":
    processor = ExcelProcessor()
    processor.process()