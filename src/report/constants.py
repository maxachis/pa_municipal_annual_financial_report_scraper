from pathlib import Path

from src.report.enums import SheetName
from src.report.models.pandera.five_year_avg_grant_by_year_and_muni import FiveYearAvgGrantByYearAndMuniSchema
from src.report.models.pandera.five_year_total_per_cap_pct_rev_grant_by_muni import \
    FiveYearTotalPerCapAndPctRevGrantByMuniSchema
from src.report.models.pandera.grant_by_year_and_muni import GrantByYearAndMuniSchema
from src.report.models.pydantic.mapping import SheetFrameMapping

OG_FILENAME: str = "MOST RECENT - SWPA Grant Revenue data - 2025.08.30.xlsx"

SWPA_PATH: Path = Path("data") / "swpa" / OG_FILENAME

OUTPUT_2015_2019_FILENAME: str = "report_2015_2019.xlsx"
OUTPUT_2020_2023_FILENAME: str = "report_2020_2023.xlsx"
OUTPUT_DIR: Path = Path("data") / "output"

SHEET_FRAME_MAPPINGS: list[SheetFrameMapping] = [
    SheetFrameMapping(
        sheet_name=SheetName.FIVE_YEAR_AVG,
        df_schema=FiveYearAvgGrantByYearAndMuniSchema,
    ),
    SheetFrameMapping(
        sheet_name=SheetName.YEAR_AND_MUNI,
        df_schema=GrantByYearAndMuniSchema,
    ),
    SheetFrameMapping(
        sheet_name=SheetName.TOTAL_PER_CAP_PCT_REV,
        df_schema=FiveYearTotalPerCapAndPctRevGrantByMuniSchema,
    ),
]

SHEET_FRAME_MAPPING_DICT: dict[SheetName, SheetFrameMapping] = {
    sheet_mapping.sheet_name: sheet_mapping for sheet_mapping in SHEET_FRAME_MAPPINGS
}