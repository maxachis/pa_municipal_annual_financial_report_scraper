from sqlalchemy import Column, Integer, ForeignKey

from src.db.models.sqlalchemy.base import StandardBase


class TotalRevenue(StandardBase):

    __tablename__ = "total_revenue"

    report_id = Column(Integer, ForeignKey("annual_reports.id"))
    total = Column(Integer)