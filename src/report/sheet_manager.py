from pandera.errors import SchemaError

from src.report.constants import SHEET_FRAME_MAPPINGS, SWPA_PATH
from src.report.enums import SheetName
import polars as pl

from src.report.exceptions import ValidateSchemaError


class SheetManager:

    def __init__(self, load_og: bool = True):
        """Loads sheets into dataframes and stores them in a dictionary"""

        self._sheet_to_df_mapping: dict[SheetName, pl.DataFrame] = {}
        if not load_og:
            return
        for sheet_mapping in SHEET_FRAME_MAPPINGS:
            df: pl.DataFrame = pl.read_excel(SWPA_PATH, sheet_name=sheet_mapping.sheet_name.value)
            try:
                sheet_mapping.df_schema.validate(df)
            except SchemaError as e:
                raise ValidateSchemaError(f"Error validating sheet {sheet_mapping.sheet_name.value}") from e
            self._sheet_to_df_mapping[sheet_mapping.sheet_name] = df

    def get_sheet(self, sheet_name: SheetName) -> pl.DataFrame:
        """Returns a sheet as a dataframe"""
        return self._sheet_to_df_mapping[sheet_name]

    def set_sheet(
        self,
        sheet_name: SheetName,
        df: pl.DataFrame
    ):
        """Sets a sheet in the dictionary"""
        self._sheet_to_df_mapping[sheet_name] = df


