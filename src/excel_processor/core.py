import re

from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from sqlalchemy.exc import IntegrityError

from src.config import REPORT_RELEVANT_SHEET_NAME, REL_TOTAL_COLUMN, REL_CODE_COLUMN, REL_LABEL_COLUMN, \
    JOINED_POP_RELEVANT_SHEET_NAME, JOINED_URBAN_RURAL_COLUMN, JOINED_GEO_COLUMN, JOINED_MUNI_COLUMN, \
    JOINED_COUNTY_COLUMN, JOINED_CLASS_COLUMN, JOINED_POP_ESTIMATE_COLUMN, JOINED_POP_MARGIN_COLUMN
from src.db.client import DatabaseClient
from src.db.models.pydantic.pop_row import PopRow
from src.db.models.sqlalchemy.enums import LocationType
from src.db.models.sqlalchemy.instantiations import JoinedPopDetailsV2
from src.excel_processor.constants import MAX_ROW, VALID_ROW_REGEX
from src.excel_processor.util import open_excel_file, case_insensitive_replace
from src.util import project_path


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
            wb = self.get_downloaded_report(report.xlsx_file)
            self.process_downloaded_report(wb, report.report_id)
            self.database_client.mark_as_processed(report.report_id)

    def get_downloaded_report(self, filename: str) -> Workbook:
        return open_excel_file(
            file_path=project_path(
                "downloads",
                filename
            )
        )

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

    def clean_county(self, county: str) -> str:
        return case_insensitive_replace(county, "County", "")

    def process_joined_pop_class_urban_rural(self):
        self.database_client.wipe_table(JoinedPopDetailsV2)
        wb = open_excel_file("Joined pop class urban rural.xlsx")


        ws: Worksheet = wb[JOINED_POP_RELEVANT_SHEET_NAME]
        pop_rows = []
        for row in ws.iter_rows(min_row=2, max_row=MAX_ROW, min_col=1, max_col=8, values_only=True):
            if row[0] is None:
                continue
            if row[0].strip() == "":
                continue
            location_type = LocationType(row[JOINED_URBAN_RURAL_COLUMN - 1])
            if location_type == LocationType.NA:
                continue

            geo = row[JOINED_GEO_COLUMN - 1]
            muni = row[JOINED_MUNI_COLUMN - 1]
            # muni = self.clean_municipality(muni)
            county = row[JOINED_COUNTY_COLUMN - 1]
            county = self.clean_county(county)
            class_ = row[JOINED_CLASS_COLUMN - 1]
            pop_estimate = row[JOINED_POP_ESTIMATE_COLUMN - 1]
            pop_margin = row[JOINED_POP_MARGIN_COLUMN - 1]
            pop_row = PopRow(
                geo_id=geo,
                county=county,
                municipality=muni,
                class_=class_,
                pop_estimate=pop_estimate,
                pop_margin=pop_margin,
                location_type=location_type
            )
            pop_rows.append(pop_row)
        self.database_client.add_pop_rows(pop_rows)
