import re
from pathlib import Path

from openpyxl import Workbook, load_workbook


def open_excel_file(file_path: Path) -> Workbook:
    return load_workbook(file_path)


def case_insensitive_replace(text, old, new):
    pattern = re.compile(re.escape(old), re.IGNORECASE)
    return pattern.sub(new, text)
