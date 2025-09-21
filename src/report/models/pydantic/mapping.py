from pandera.api.polars.model import DataFrameModel
from pydantic import BaseModel

from src.report.enums import SheetName


class SheetFrameMapping(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    sheet_name: SheetName
    df_schema: type[DataFrameModel]