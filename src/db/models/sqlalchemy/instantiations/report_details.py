from sqlalchemy import Column, Integer, UniqueConstraint, ForeignKey

from src.db.models.sqlalchemy.base import StandardBase
from src.db.models.sqlalchemy.mixins import AnnualReportMixin


class ReportDetails(
    StandardBase,
    AnnualReportMixin
):
    __tablename__ = "report_details"
    __table_args__ = (
        UniqueConstraint(
            "report_id",
            "code_id",
            name="report_details_uq_report_code"
        ),
    )

    code_id = Column(Integer, ForeignKey("codes_v2.id"), nullable=True)
    total = Column(Integer, nullable=True)
