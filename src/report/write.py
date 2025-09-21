from pathlib import Path

from src.report.constants import OUTPUT_DIR
from src.report.enums import SheetName
from src.report.models.pandera.five_year_avg_grant_by_year_and_muni import FiveYearAvgGrantByYearAndMuniSchema
from src.report.models.pandera.five_year_total_per_cap_pct_rev_grant_by_muni import \
    FiveYearTotalPerCapAndPctRevGrantByMuniSchema
from src.report.models.pandera.grant_by_year_and_muni import GrantByYearAndMuniSchema
from src.report.sheet_manager import SheetManager

from xlsxwriter import Workbook

from pandera.typing.polars import DataFrame

import polars as pl

def write_year_and_muni(df: DataFrame[GrantByYearAndMuniSchema], wb: Workbook) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["County", "Municipality", "Year"]
    )
    sorted_df.write_excel(
        workbook = wb,
        worksheet = SheetName.YEAR_AND_MUNI.value,
        dtype_formats = {
            dt: "####" for dt in [pl.Int32, pl.Int64]
        },
    )

def write_five_year_avg(df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema], wb: Workbook) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["COUNTY", "MUNICIPALITY"]
    )
    sorted_df.write_excel(
        workbook = wb,
        worksheet = SheetName.FIVE_YEAR_AVG.value,
        dtype_formats = {
            dt: "##,###,###.00" for dt in [pl.Float32, pl.Float64]
        },
    )

def write_per_capita(df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema], wb: Workbook) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["COUNTY", "MUNICIPALITY"]
    )
    sorted_df.write_excel(
        workbook = wb,
        worksheet = SheetName.TOTAL_PER_CAP_PCT_REV.value,
        dtype_formats = {
            dt: "#,###,###,###.00" for dt in [pl.Float32, pl.Float64]
        },
    )

def write_sheet_manager_to_excel(
    sm: SheetManager,
    filename: str
) -> None:
    output_path: Path = OUTPUT_DIR / filename

    with Workbook(output_path) as wb:
        # Year and Muni
        by_year_muni_df = GrantByYearAndMuniSchema.validate(sm.get_sheet(SheetName.YEAR_AND_MUNI))
        write_year_and_muni(by_year_muni_df, wb=wb)
        # Five Year Avg
        by_five_year_avg_df = FiveYearAvgGrantByYearAndMuniSchema.validate(sm.get_sheet(SheetName.FIVE_YEAR_AVG))
        write_five_year_avg(by_five_year_avg_df, wb=wb)

        # Per Capita
        per_capita_df = FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(sm.get_sheet(SheetName.TOTAL_PER_CAP_PCT_REV))
        write_per_capita(per_capita_df, wb=wb)
