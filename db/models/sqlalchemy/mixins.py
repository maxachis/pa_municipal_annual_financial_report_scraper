from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship


class CountyMixin:
    county_id = Column(Integer, ForeignKey("counties.id"))

    county = relationship("County")

class MunicipalityMixin:
    municipality_id = Column(Integer, ForeignKey("municipalities.id"))

    municipality = relationship("Municipality")

class AnnualReportMixin:
    report_id = Column(Integer, ForeignKey("reports.id"))

    report = relationship("AnnualReport")

