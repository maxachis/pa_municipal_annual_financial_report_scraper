from openpyxl.workbook import Workbook

from database_logic.DatabaseManager import DatabaseManager
from report_creator.data_objects import CMYBreakdownRow


class ReportCreator:

    def __init__(self, report_name: str):
        self.report_name = report_name
        self.workbook = Workbook()

    def breakdown_sheet(self, row_breakdowns: list[CMYBreakdownRow]):
        ws = self.workbook.active
        ws.title = "Breakdown"
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

        self.workbook.save(self.report_name)


if __name__ == "__main__":
    dm = DatabaseManager()
    rows = dm.get_row_breakdowns()

    rc = ReportCreator("report.xlsx")
    rc.breakdown_sheet(rows)
