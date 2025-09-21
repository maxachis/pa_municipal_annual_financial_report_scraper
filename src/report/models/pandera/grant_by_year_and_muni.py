

from pandera.polars import DataFrameModel, Field
from pandera.typing.polars import Series

from src.report.enums import YEAR_VALUES


class GrantByYearAndMuniSchema(DataFrameModel):
    county: Series[str] = Field(alias="County")
    municipality: Series[str] = Field(alias="Municipality")
    year: Series[int] = Field(alias="Year", isin=YEAR_VALUES, coerce=True)
    total_revenue: Series[int] = Field(
        alias="Total revenue",
        nullable=True,
        coerce=True
    )
    federal_grants: Series[int] = Field(alias="Federal Grants")
    state_grants: Series[int] = Field(alias="State Grants")
    local_grants: Series[int] = Field(alias="Local Grants")
    all_grants: Series[int] = Field(alias="All grants")
