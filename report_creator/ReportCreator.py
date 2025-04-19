"""
This page contains both the ReportCreator class
as well as a main method which operates the class
"""

from openpyxl.workbook import Workbook

from database_logic.DatabaseManager import DatabaseManager
from report_creator.data_objects import CMYBreakdownRow, AverageRow


class ReportCreator:
    """
    The ReportCreator class is responsible for creating
    and saving the final excel report
    """

    def __init__(self, report_name: str):
        self.report_name = report_name
        self.workbook = Workbook()

    def breakdown_sheet(self, row_breakdowns: list[CMYBreakdownRow]):
        """
        Creates the breakdown sheet
        :param row_breakdowns:
        :return:
        """
        ws = self.workbook.active
        ws.title = "Breakdown"
        # Set the column headers
        ws.append(
            [
                "County",
                "Municipality",
                "Year",
                "Federal Subtotal",
                "State Subtotal",
                "Local Subtotal",
                "Total"
            ]
        )
        # Add the breakdown rows to the sheet
        for row in row_breakdowns:
            ws.append(
                [
                    row.county,
                    row.municipality,
                    row.year,
                    row.federal_amt,
                    row.state_amt,
                    row.local_amt,
                    row.get_total()
                ]
            )



    def average_sheet(self, average_rows: list[AverageRow]):
        """
        Creates the average sheet
        :param average_rows:
        :return:
        """
        ws = self.workbook.create_sheet("Average")
        # Set the column headers
        ws.append(
            [
                "County",
                "Municipality",
                "Federal Average",
                "State Average",
                "Local Average",
            ]
        )
        # Add the average rows to the sheet
        for row in average_rows:
            ws.append(
                [
                    row.county,
                    row.municipality,
                    row.federal_average,
                    row.state_average,
                    row.local_average,
                ]
            )


if __name__ == "__main__":
    # Initialize the database manager
    # And retrieve necessary data from the database
    dm = DatabaseManager()
    rows = dm.get_row_breakdowns()
    average_rows = dm.get_county_municipality_averages()

    # Initialize the report creator and create all sheets
    rc = ReportCreator("report.xlsx")
    rc.breakdown_sheet(rows)
    rc.average_sheet(average_rows)

    # Save the report
    rc.workbook.save(filename=rc.report_name)
