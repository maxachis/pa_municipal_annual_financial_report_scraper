from sqlalchemy import Column, Integer, ForeignKey

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.mixins import ViewMixin


class StateTotalPerReport(ViewMixin, Base):

    __tablename__ = "state_total_per_report"

    report_id = Column(Integer, ForeignKey("annual_reports.id"), primary_key=True)
    report_total = Column(Integer)