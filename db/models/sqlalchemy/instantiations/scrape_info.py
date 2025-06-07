from sqlalchemy import UniqueConstraint, String, Column

from db.models.sqlalchemy.base import StandardBase
from db.models.sqlalchemy.mixins import AnnualReportMixin


class ScrapeInfo(
    StandardBase,
    AnnualReportMixin
):
    __tablename__ = "scrape_info"
    __table_args__ = (
        UniqueConstraint(
            "report_id",
            name="scrape_info_uq_report"
        ),
        UniqueConstraint(
            "filename",
            name="scrape_info_uq_filename"
        )
    )
    filename = Column(String, nullable=True)
