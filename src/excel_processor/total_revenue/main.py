"""
Run to scrape total revenue from all files
"""
from openpyxl import Workbook
from tqdm import tqdm
from openpyxl.worksheet.worksheet import Worksheet
from src.config import REPORT_RELEVANT_SHEET_NAME, REL_TOTAL_COLUMN
from src.db.client import DatabaseClient
from src.excel_processor.constants import MAX_ROW
from src.excel_processor.load import load_downloaded_report
from src.excel_processor.total_revenue.models.file_report_mapping import FileReportMapping
from src.excel_processor.total_revenue.queries.get import GetReportsMissingTotalRevenueQueryBuilder
from src.excel_processor.total_revenue.queries.insert import InsertTotalRevenueQueryBuilder


def get_total_revenue_from_file(filename: str) -> float:
    wb: Workbook = load_downloaded_report(filename)
    ws: Worksheet = wb[REPORT_RELEVANT_SHEET_NAME]
    for row in ws.iter_rows(
        min_row=1,
        max_row=MAX_ROW,
        min_col=1,
        max_col=REL_TOTAL_COLUMN,
        values_only=True
    ):

        if row[1] != "TOTAL REVENUES":
            continue

        total: int = row[REL_TOTAL_COLUMN - 1]
        return total

    raise ValueError("Total revenues not found")



def main():
    dbc = DatabaseClient()
    inputs: list[FileReportMapping] = dbc.run_query_builder(GetReportsMissingTotalRevenueQueryBuilder())
    for input_ in tqdm(inputs):
        total_revenue = get_total_revenue_from_file(input_.filename)
        dbc.run_query_builder(InsertTotalRevenueQueryBuilder(report_id=input_.report_id, total_revenue=total_revenue))

if __name__ == "__main__":
    main()