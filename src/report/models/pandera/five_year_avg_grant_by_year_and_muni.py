

from pandera.polars import DataFrameModel, Field
from pandera.typing.polars import Series

from src.report.enums import MUNICIPALITY_CLASS_VALUES, URBAN_RURAL_VALUES


class FiveYearAvgGrantByYearAndMuniSchema(DataFrameModel):
    county: Series[str] = Field(alias="COUNTY")
    municipality: Series[str] = Field(alias="MUNICIPALITY")
    class_: Series[str] = Field(
        alias="CLASS",
        isin=MUNICIPALITY_CLASS_VALUES
    )
    urban_rural: Series[str] = Field(
        alias="URBAN/RURAL",
        isin=URBAN_RURAL_VALUES
    )
    federal_5_year_avg: Series[float] = Field(
        alias=" FEDERAL 5-YEAR AVERAGE",
        ge=0,
        coerce=True
    )
    state_5_year_avg: Series[float] = Field(
        alias="STATE 5-YEAR AVERAGE",
        ge=0,
        coerce=True
    )
    local_5_year_avg: Series[float] = Field(
        alias="LOCAL 5-YEAR AVERAGE",
        ge=0,
        coerce=True
    )
    total_5_year_avg: Series[float] = Field(
        alias="TOTAL 5-YEAR AVERAGE",
        ge=0,
        coerce=True
    )