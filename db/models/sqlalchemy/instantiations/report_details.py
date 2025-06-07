from sqlalchemy import Column, Integer

from db.models.sqlalchemy.base import StandardBase
from db.models.sqlalchemy.mixins import AnnualReportMixin


class ReportDetails(
    StandardBase,
    AnnualReportMixin
):
    __tablename__ = "report_details"

    total = Column(Integer, nullable=True)