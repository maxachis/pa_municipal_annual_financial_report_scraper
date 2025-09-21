from pandera.errors import SchemaError

from src.report.constants import SHEET_FRAME_MAPPING_DICT
from src.report.enums import SheetName
import polars as pl

from src.report.exceptions import ValidateSchemaError


def validate_sheet(df: pl.DataFrame, sheet: SheetName) -> None:
    """
    Raises ValidateSchemaError if the sheet is not valid
    """

    sheet_mapping = SHEET_FRAME_MAPPING_DICT.get(sheet)
    if sheet_mapping is None:
        raise ValidateSchemaError(f"Sheet {sheet.value} not found")

    try:
        sheet_mapping.df_schema.validate(df)
    except SchemaError as e:
        raise ValidateSchemaError(f"Error validating sheet {sheet.value}") from e