from src.report.constants import OUTPUT_2015_2019_FILENAME, OUTPUT_2020_2023_FILENAME
from src.report.process.core import process_2015_2019, process_2020_2023
from src.report.sheet_manager import SheetManager
from src.report.write import write_sheet_manager_to_excel


def main() -> None:
    sm_2015_2019: SheetManager = process_2015_2019()
    write_sheet_manager_to_excel(sm_2015_2019, filename=OUTPUT_2015_2019_FILENAME)

    sm_2020_2023: SheetManager = process_2020_2023()
    write_sheet_manager_to_excel(sm_2020_2023, filename=OUTPUT_2020_2023_FILENAME)


if __name__ == "__main__":
    main()