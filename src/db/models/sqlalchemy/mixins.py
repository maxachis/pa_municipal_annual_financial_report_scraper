from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declared_attr, Mapped


class CountyMixin:
    county_id = Column(Integer, ForeignKey("counties.id"))

    @declared_attr
    def county(cls) -> Mapped["County"]:
        return relationship("County")


class MunicipalityMixin:
    municipality_id = Column(Integer, ForeignKey("municipalities.id"))


    @declared_attr
    def municipality(self) -> Mapped["Municipality"]:
        return relationship("Municipality")

class AnnualReportMixin:
    report_id = Column(Integer, ForeignKey("annual_reports.id"))

    @declared_attr
    def report(self) -> Mapped["AnnualReport"]:
        return relationship("AnnualReport")

class IDMixin:
    id = Column(Integer, primary_key=True, index=True)

class CreatedAtMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )