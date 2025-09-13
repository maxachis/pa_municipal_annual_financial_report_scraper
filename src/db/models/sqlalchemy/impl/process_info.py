from sqlalchemy import UniqueConstraint

from src.db.models.sqlalchemy.base import StandardBase
from src.db.models.sqlalchemy.mixins import AnnualReportMixin


class ProcessInfo(
    StandardBase,
    AnnualReportMixin
):
    __tablename__ = "process_info"
    __table_args__ = (
        UniqueConstraint(
            "report_id",
            name="process_info_uq_report"
        ),
    )
