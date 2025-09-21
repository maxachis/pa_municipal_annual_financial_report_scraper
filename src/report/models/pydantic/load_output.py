from pydantic import BaseModel

from src.report.models.pandera.five_year_avg_grant_by_year_and_muni import FiveYearAvgGrantByYearAndMuniSchema
from src.report.models.pandera.five_year_total_per_cap_pct_rev_grant_by_muni import \
    FiveYearTotalPerCapAndPctRevGrantByMuniSchema
from src.report.models.pandera.grant_by_year_and_muni import GrantByYearAndMuniSchema


class LoadOutput(BaseModel):
    by_year: GrantByYearAndMuniSchema
    five_year_avg: FiveYearAvgGrantByYearAndMuniSchema
    total_per_cap_pct_rev: FiveYearTotalPerCapAndPctRevGrantByMuniSchema