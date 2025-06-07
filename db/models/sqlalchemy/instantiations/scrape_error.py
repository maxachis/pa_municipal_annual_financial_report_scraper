from sqlalchemy import UniqueConstraint, String, Column

from db.models.sqlalchemy.base import StandardBase
from db.models.sqlalchemy.mixins import AnnualReportMixin


class ScrapeError(
    StandardBase,
    AnnualReportMixin
):
    __table_name__ = "scrape_error"
    __table_args__ = (
        UniqueConstraint(
            "report_id",
            name="scrape_error_uq_report_id"
        ),
    )

    message = Column(String)