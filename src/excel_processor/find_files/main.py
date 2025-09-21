"""
Run to match all files to the database
"""
from src.db.client import DatabaseClient
from src.excel_processor.find_files.constants import DOWNLOADS_DIRECTORY
from src.excel_processor.find_files.models.input_ import FindFilesInput
from src.excel_processor.find_files.models.insert import ReportFileInsert
from src.excel_processor.find_files.queries.get import GetReportsMissingFilesQuery
import os

from src.excel_processor.find_files.queries.insert import InsertReportFileQueryBuilder


def get_downloaded_file_names() -> set[str]:
    return set(os.listdir(DOWNLOADS_DIRECTORY))

def build_filename(input_: FindFilesInput) -> str:
    return f"report_{input_.county_name}_{input_.municipality_name}_{input_.year}.xlsx"

def main() -> None:
    dbc = DatabaseClient()
    inputs: list[FindFilesInput] = dbc.run_query_builder(GetReportsMissingFilesQuery())
    downloaded_filenames: set[str] = get_downloaded_file_names()
    for input_ in inputs:
        built_filename = build_filename(input_)
        if built_filename in downloaded_filenames:
            print(f"Found file: {built_filename}. Updating database...")
            qb = InsertReportFileQueryBuilder(
                report_file=ReportFileInsert(
                    report_id=input_.scrape_info_id,
                    file_name=built_filename
                )
            )
            dbc.run_query_builder(qb)






if __name__ == "__main__":
    main()