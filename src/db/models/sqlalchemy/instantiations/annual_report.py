from sqlalchemy import UniqueConstraint, Column, Integer
from sqlalchemy.orm import relationship

from src.db.models.sqlalchemy.base import StandardBase
from src.db.models.sqlalchemy.mixins import CountyMixin, MunicipalityMixin


class AnnualReport(
    StandardBase,
    CountyMixin,
    MunicipalityMixin
):
    __tablename__ = "annual_reports"
    __table_args__ = (
        UniqueConstraint(
            "county_id",
            "municipality_id",
            "year",
            name="annual_report_uq_county_municipality_year"
        ),
    )
    year = Column(Integer)
    scrape_info = relationship(
        "ScrapeInfo",
        back_populates="report"
    )
    process_info = relationship(
        "ProcessInfo",
        back_populates="report"
    )
