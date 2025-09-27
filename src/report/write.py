import re
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

def write_year_and_muni(
    df: DataFrame[GrantByYearAndMuniSchema],
    wb: Workbook
) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["County", "Municipality", "Year"]
    )
    column_order = [
        "County",
        "Municipality",
        "Year",
        "Total revenue",
        "Federal Grants",
        "State Grants",
        "Local Grants",
        "All grants"
    ]
    reordered_df: pl.DataFrame = sorted_df.select(column_order)
    reordered_df.write_excel(
        workbook = wb,
        worksheet = SheetName.YEAR_AND_MUNI.value,
        dtype_formats = {
            dt: "0" for dt in [pl.Int32, pl.Int64]
        },
        autofit=True
    )

def replace_years(col_name: str) -> str:
    return col_name.replace("5", "4")

def write_five_year_avg(
    df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema],
    wb: Workbook,
    replace_5_year: bool = False
) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["COUNTY", "MUNICIPALITY"]
    )
    column_order = [
        "COUNTY",
        "MUNICIPALITY",
        "CLASS",
        "URBAN/RURAL",
        " FEDERAL 5-YEAR AVERAGE",
        "STATE 5-YEAR AVERAGE",
        "LOCAL 5-YEAR AVERAGE",
        "TOTAL 5-YEAR AVERAGE"
    ]
    reordered_df: pl.DataFrame = sorted_df.select(column_order)
    if replace_5_year:
        reordered_df = reordered_df.rename({
            col_name: replace_years(col_name) for col_name in column_order
        })
        worksheet_name: str = SheetName.FIVE_YEAR_AVG.value.replace("5", "4")
    else:
        worksheet_name: str = SheetName.FIVE_YEAR_AVG.value

    reordered_df.write_excel(
        workbook = wb,
        worksheet = worksheet_name,
        dtype_formats = {
            dt: "##,###,###.00" for dt in [pl.Float32, pl.Float64]
        },
        header_format = {
            "bold": True,
            'font_name': 'Arial',
            'font_size': 11,
            'bg_color': '#BDBDBD'
        },
        autofit=True
    )

def write_per_capita(
    df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema],
    wb: Workbook,
    replace_5_year: bool = False
) -> None:
    sorted_df: pl.DataFrame = df.sort(
        by=["COUNTY", "MUNICIPALITY"]
    )
    column_order = [
        "GEOID",
        "COUNTY",
        "MUNICIPALITY",
        "CLASS",
        "URBAN/RURAL",
        "POPULATION ESTIMATE",
        "POPULATION MARGIN",
        "FEDERAL GRANTS 5-YEAR TOTAL",
        "STATE GRANTS 5-YEAR TOTAL",
        "LOCAL GRANTS 5-YEAR TOTAL",
        "ALL GRANTS 5-YEAR TOTAL",
        "FEDERAL GRANTS 5-YR TOTAL PER CAPITA",
        "STATE GRANTS 5-YR TOTAL PER CAPITA",
        "LOCAL GRANTS 5-YR TOTAL PER CAPITA",
        "ALL GRANTS 5-YR TOTAL PER CAPITA",
        "TOTAL REVENUE 5-YEAR TOTAL",
        "% REV FED GRANTS",
        "% REV STATE GRANTS",
        "% REV LOCAL GRANTS",
        "% REV ALL GRANTS"
    ]
    reordered_df: pl.DataFrame = sorted_df.select(column_order)
    if replace_5_year:
        reordered_df = reordered_df.rename({
            col_name: replace_years(col_name) for col_name in column_order
        })
        worksheet_name: str = SheetName.TOTAL_PER_CAP_PCT_REV.value.replace("5", "4")
    else:
        worksheet_name: str = SheetName.TOTAL_PER_CAP_PCT_REV.value

    reordered_df.write_excel(
        workbook = wb,
        worksheet = worksheet_name,
        dtype_formats = {
            dt: "#,###,###,###.00" for dt in [pl.Float32, pl.Float64]
        },
        column_formats={
            "% REV FED GRANTS": "0.00%",
            "% REV STATE GRANTS": "0.00%",
            "% REV LOCAL GRANTS": "0.00%",
            "% REV ALL GRANTS": "0.00%",
        },
        header_format={
            "bold": True,
            'font_name': 'Arial',
            'font_size': 11,
            'bg_color': '#BDBDBD'
        },
        autofit=True
    )

def write_sheet_manager_to_excel(
    sm: SheetManager,
    filename: str,
    replace_5_year: bool = False
) -> None:
    output_path: Path = OUTPUT_DIR / filename

    with Workbook(output_path) as wb:
        # Year and Muni
        by_year_muni_df = GrantByYearAndMuniSchema.validate(sm.get_sheet(SheetName.YEAR_AND_MUNI))
        write_year_and_muni(by_year_muni_df, wb=wb)
        # Five Year Avg
        by_five_year_avg_df = FiveYearAvgGrantByYearAndMuniSchema.validate(sm.get_sheet(SheetName.FIVE_YEAR_AVG))
        write_five_year_avg(by_five_year_avg_df, wb=wb, replace_5_year=replace_5_year)

        # Per Capita
        per_capita_df = FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(sm.get_sheet(SheetName.TOTAL_PER_CAP_PCT_REV))
        write_per_capita(per_capita_df, wb=wb, replace_5_year=replace_5_year)
