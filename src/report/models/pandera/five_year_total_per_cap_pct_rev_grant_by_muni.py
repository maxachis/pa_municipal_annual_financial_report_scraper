from pandera.polars import DataFrameModel, Field
from pandera.typing.polars import Series

from src.report.enums import MUNICIPALITY_CLASS_VALUES, URBAN_RURAL_VALUES


class FiveYearTotalPerCapAndPctRevGrantByMuniSchema(DataFrameModel):
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
    population_estimate: Series[int] = Field(
        alias="POPULATION ESTIMATE",
        coerce=True
    )
    population_margin: Series[int] = Field(
        alias="POPULATION MARGIN",
        nullable=True,
        coerce=True
    )
    federal_grants_5_year_total: Series[int] = Field(
        alias="FEDERAL GRANTS 5-YEAR TOTAL",
        nullable=True,
        coerce=True
    )
    state_grants_5_year_total: Series[int] = Field(
        alias="STATE GRANTS 5-YEAR TOTAL",
        coerce=True
    )
    local_grants_5_year_total: Series[int] = Field(
        alias="LOCAL GRANTS 5-YEAR TOTAL",
        coerce=True
    )
    all_grants_5_year_total: Series[int] = Field(
        alias="ALL GRANTS 5-YEAR TOTAL",
        coerce=True
    )
    federal_grants_5_year_total_per_capita: Series[float] = Field(
        alias="FEDERAL GRANTS 5-YR TOTAL PER CAPITA",
        coerce=True,
        nullable=True
    )
    state_grants_5_year_total_per_capita: Series[float] = Field(
        alias="STATE GRANTS 5-YR TOTAL PER CAPITA",
        coerce=True,
        nullable=True
    )
    local_grants_5_year_total_per_capita: Series[float] = Field(
        alias="LOCAL GRANTS 5-YR TOTAL PER CAPITA",
        coerce=True,
        nullable=True
    )
    all_grants_5_year_total_per_capita: Series[float] = Field(
        alias="ALL GRANTS 5-YR TOTAL PER CAPITA",
        coerce=True,
        nullable=True
    )
    total_revenue_5_year_total: Series[int] = Field(alias="TOTAL REVENUE 5-YEAR TOTAL", nullable=True, coerce=True)
    pct_rev_fed_grants: Series[float] = Field(alias="% REV FED GRANTS", nullable=True, coerce=True)
    pct_rev_state_grants: Series[float] = Field(alias="% REV STATE GRANTS", nullable=True, coerce=True)
    pct_rev_local_grants: Series[float] = Field(alias="% REV LOCAL GRANTS", nullable=True, coerce=True)
    pct_rev_all_grants: Series[float] = Field(alias="% REV ALL GRANTS", nullable=True, coerce=True)