from openpyxl import Workbook

from src.excel_processor.util import open_excel_file
from src.util import project_path


def load_downloaded_report(filename: str) -> Workbook:
    return open_excel_file(
        file_path=project_path(
            "downloads",
            filename
        )
    )
