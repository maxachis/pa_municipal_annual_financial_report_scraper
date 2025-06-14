from src.db.client import DatabaseClient
from src.report_creator.ReportCreator import ReportCreator

if __name__ == "__main__":
    # Initialize the database manager
    # And retrieve necessary data from the database
    dm = DatabaseClient()
    rows = dm.get_row_breakdowns()
    average_rows = dm.get_average_with_pop_rows()

    # Initialize the report creator and create all sheets
    rc = ReportCreator("report.xlsx")
    rc.breakdown_sheet(rows)
    rc.average_sheet(average_rows)

    # Save the report
    rc.workbook.save(filename=rc.report_name)
