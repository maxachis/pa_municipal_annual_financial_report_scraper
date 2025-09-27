from pandera.typing.polars import DataFrame
from src.report.process.load import load_by_year_muni, load_by_five_year_avg, load_by_per_capita
from src.report.enums import SheetName, YearCond
from src.report.models.pandera.five_year_avg_grant_by_year_and_muni import FiveYearAvgGrantByYearAndMuniSchema
from src.report.models.pandera.five_year_total_per_cap_pct_rev_grant_by_muni import \
    FiveYearTotalPerCapAndPctRevGrantByMuniSchema
from src.report.models.pandera.grant_by_year_and_muni import GrantByYearAndMuniSchema
from src.report.sheet_manager import SheetManager
import polars as pl


def merge_existing_counties_by_year_muni(
    og_df: DataFrame[GrantByYearAndMuniSchema],
    new_df: DataFrame[GrantByYearAndMuniSchema]
) -> DataFrame[GrantByYearAndMuniSchema]:
    # Filter new_df to existing counties
    filtered_new_df: DataFrame[GrantByYearAndMuniSchema] = new_df.filter(
        new_df["County"].is_in(og_df["County"])
        & new_df["Municipality"].is_in(og_df["Municipality"])
        & new_df["Year"].is_in(og_df["Year"])
    )
    # Get only subset of columns from filtered_new_df
    select_new_df: DataFrame[GrantByYearAndMuniSchema] = filtered_new_df.select(
        ["County", "Municipality", "Year", "Total revenue"]
    )
    # Drop non-join columns from og_df
    drop_og_df = og_df.drop(
        ["Total revenue"]
    )
    # Join select_new_df with og_df on County, Municipality, Year
    joined_df: DataFrame[GrantByYearAndMuniSchema] = select_new_df.join(
        drop_og_df,
        on=["County", "Municipality", "Year"]
    )
    return GrantByYearAndMuniSchema.validate(joined_df)

def add_new_counties_by_year_muni(
    og_df: DataFrame[GrantByYearAndMuniSchema],
    new_df: DataFrame[GrantByYearAndMuniSchema]
) -> DataFrame[GrantByYearAndMuniSchema]:
    # Filter to only new counties
    filtered_new_df: DataFrame[GrantByYearAndMuniSchema] = new_df.join(
        og_df,
        on=["County", "Municipality", "Year"],
        how="anti",
    )
    return GrantByYearAndMuniSchema.validate(
        GrantByYearAndMuniSchema.validate(og_df).vstack(filtered_new_df)
    )

def add_new_counties_five_year_avg(
    og_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema],
    new_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema]
) -> DataFrame[FiveYearAvgGrantByYearAndMuniSchema]:
    # Filter to only new counties
    filtered_new_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema] = new_df.filter(
        ~new_df["COUNTY"].is_in(og_df["COUNTY"])
    )
    return FiveYearAvgGrantByYearAndMuniSchema.validate(
        FiveYearAvgGrantByYearAndMuniSchema.validate(og_df).vstack(filtered_new_df)
    )

def merge_existing_counties_per_capita(
    og_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema],
    new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]
) -> DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]:
    # Filter to only existing counties
    filtered_new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = new_df.filter(
        new_df["COUNTY"].is_in(og_df["COUNTY"])
    )
    # Get only subset of columns from filtered_new_df
    select_new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = filtered_new_df.select(
        [
            "COUNTY",
            "MUNICIPALITY",
            "TOTAL REVENUE 5-YEAR TOTAL",
            "% REV FED GRANTS",
            "% REV STATE GRANTS",
            "% REV LOCAL GRANTS",
            "% REV ALL GRANTS"
        ]
    )
    # Drop non-join columns from og_df
    drop_og_df = og_df.drop(
        [
            "TOTAL REVENUE 5-YEAR TOTAL",
            "% REV FED GRANTS",
            "% REV STATE GRANTS",
            "% REV LOCAL GRANTS",
            "% REV ALL GRANTS"
        ]
    )
    # Join select_new_df with drop_og_df on County, Municipality
    joined_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = select_new_df.join(
        drop_og_df,
        on=["COUNTY", "MUNICIPALITY"]
    )
    return FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(joined_df)


def add_new_counties_per_capita(
    og_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema],
    new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]
) -> DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]:
    # Filter to only new counties
    filtered_new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = new_df.filter(
        ~new_df["COUNTY"].is_in(og_df["COUNTY"])
    )
    reindexed_new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = filtered_new_df.select(
        og_df.columns
    )
    return FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(
        FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(og_df).vstack(reindexed_new_df)
    )

def process_by_five_year_avg(
    og_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema]
) -> DataFrame[FiveYearAvgGrantByYearAndMuniSchema]:
    new_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema] = load_by_five_year_avg()
    return FiveYearAvgGrantByYearAndMuniSchema.validate(
        FiveYearAvgGrantByYearAndMuniSchema.validate(og_df).vstack(new_df)
    )

def apply_per_capita_spot_corrections(
    df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]
) -> DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]:
    return df.with_columns(
        pl.when(
            (pl.col("COUNTY") == "WESTMORELAND") & (pl.col("MUNICIPALITY") == "MCDONALD BORO"))
            .then(pl.lit("WASHINGTON"))
            .otherwise(pl.col("COUNTY"))
            .alias("COUNTY")
    )

def process_2015_2019() -> SheetManager:
    sm = SheetManager()

    # By Year
    by_year_new_df: DataFrame[GrantByYearAndMuniSchema] = load_by_year_muni(YearCond.Y2015_2019)
    by_year_og_df: DataFrame[GrantByYearAndMuniSchema] = sm.get_sheet(SheetName.YEAR_AND_MUNI)
    by_year_og_df = merge_existing_counties_by_year_muni(by_year_og_df, by_year_new_df)
    by_year_og_df = add_new_counties_by_year_muni(by_year_og_df, by_year_new_df)
    sm.set_sheet(SheetName.YEAR_AND_MUNI, by_year_og_df)

    # Five Year Average
    five_year_new_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema] = load_by_five_year_avg(YearCond.Y2015_2019)
    five_year_og_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema] = sm.get_sheet(SheetName.FIVE_YEAR_AVG)
    five_year_og_df = add_new_counties_five_year_avg(five_year_og_df, five_year_new_df)
    sm.set_sheet(SheetName.FIVE_YEAR_AVG, five_year_og_df)

    # Per Capita
    per_capita_new_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = load_by_per_capita(YearCond.Y2015_2019)
    per_capita_og_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = sm.get_sheet(SheetName.TOTAL_PER_CAP_PCT_REV)
    per_capita_og_spot_correct_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = apply_per_capita_spot_corrections(per_capita_og_df)
    per_capita_merge_df = merge_existing_counties_per_capita(per_capita_og_spot_correct_df, per_capita_new_df)
    per_capita_add_df = add_new_counties_per_capita(per_capita_merge_df, per_capita_new_df)
    sm.set_sheet(SheetName.TOTAL_PER_CAP_PCT_REV, per_capita_add_df)

    return sm

def process_2020_2023() -> SheetManager:
    sm = SheetManager(load_og=False)

    by_year_df: DataFrame[GrantByYearAndMuniSchema] = load_by_year_muni(YearCond.Y2020_2023)
    sm.set_sheet(SheetName.YEAR_AND_MUNI, by_year_df)

    five_year_df: DataFrame[FiveYearAvgGrantByYearAndMuniSchema] = load_by_five_year_avg(YearCond.Y2020_2023)
    sm.set_sheet(SheetName.FIVE_YEAR_AVG, five_year_df)

    per_capita_df: DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema] = load_by_per_capita(YearCond.Y2020_2023)
    sm.set_sheet(SheetName.TOTAL_PER_CAP_PCT_REV, per_capita_df)

    return sm
