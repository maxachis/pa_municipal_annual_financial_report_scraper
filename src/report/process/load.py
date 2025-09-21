import polars as pl
from pandera.typing.polars import DataFrame

from src.db.constants import DB_CONNECTION_STRING
from src.report.process.queries.by_year_muni import GET_BY_YEAR_MUNI_SCRIPT
from src.report.process.queries.five_year_avg import GET_FIVE_YEAR_AVG_SCRIPT
from src.report.process.queries.per_capita import GET_PER_CAPITA_SCRIPT
from src.report.enums import YearCond
from src.report.models.pandera.five_year_avg_grant_by_year_and_muni import FiveYearAvgGrantByYearAndMuniSchema
from src.report.models.pandera.five_year_total_per_cap_pct_rev_grant_by_muni import \
    FiveYearTotalPerCapAndPctRevGrantByMuniSchema
from src.report.models.pandera.grant_by_year_and_muni import GrantByYearAndMuniSchema


def load_by_year_muni(yc: YearCond) -> DataFrame[GrantByYearAndMuniSchema]:
    df: pl.DataFrame = pl.read_database_uri(
        GET_BY_YEAR_MUNI_SCRIPT.format(year_cond=yc.value),
        uri=DB_CONNECTION_STRING
    )
    return GrantByYearAndMuniSchema.validate(df)

def load_by_five_year_avg(yc: YearCond) -> DataFrame[FiveYearAvgGrantByYearAndMuniSchema]:
    df: pl.DataFrame = pl.read_database_uri(
        GET_FIVE_YEAR_AVG_SCRIPT.format(year_cond=yc.value),
        uri=DB_CONNECTION_STRING
    )
    return FiveYearAvgGrantByYearAndMuniSchema.validate(df)

def load_by_per_capita(yc: YearCond) -> DataFrame[FiveYearTotalPerCapAndPctRevGrantByMuniSchema]:
    df: pl.DataFrame = pl.read_database_uri(
        GET_PER_CAPITA_SCRIPT.format(year_cond=yc.value),
        uri=DB_CONNECTION_STRING
    )
    return FiveYearTotalPerCapAndPctRevGrantByMuniSchema.validate(df)