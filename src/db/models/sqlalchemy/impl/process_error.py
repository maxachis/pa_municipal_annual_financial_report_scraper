from sqlalchemy import Column, String, UniqueConstraint

from src.db.models.sqlalchemy.base import StandardBase
from src.db.models.sqlalchemy.mixins import AnnualReportMixin


class ProcessError(
    StandardBase,
    AnnualReportMixin
):
    __tablename__ = "process_errors"
    __table_args__ = (
        UniqueConstraint(
            "report_id",
            name="process_error_uq_report"
        ),
    )

    message = Column(String)
