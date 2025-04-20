from sqlalchemy import Column, String, Integer, Enum, Float
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Code(Base):
    """
    Represents a code and its label
    """
    __tablename__ = "codes"
    code = Column(String, primary_key=True)
    label = Column(String)


class AnnualFinancialReportDetails(Base):
    """
    Represents a total value for an annual financial report
    Organized by the county, municipality, and year for the report
    As well as a code within the report
    """
    __tablename__ = "annual_financial_report_details"
    county = Column(String, primary_key=True)
    municipality = Column(String, primary_key=True)
    year = Column(String, primary_key=True)
    code = Column(String, primary_key=True)
    total = Column(Integer, nullable=True)

class JoinedPopDetails(Base):
    __tablename__ = "joined_pop_details"
    geo_id = Column(String, primary_key=True)
    county = Column(String)
    municipality = Column(String)
    class_ = Column(String)
    pop_estimate = Column(Integer)
    pop_margin = Column(Integer)
    urban_rural = Column(String)

class IntermediateTable(Base):
    __tablename__ = "intermediate_table"
    geo_id = Column(String, primary_key=True)
    county_downloaded = Column(String, primary_key=True)
    municipality_downloaded = Column(String, primary_key=True)
    county_joined = Column(String, primary_key=True)
    municipality_joined = Column(String, primary_key=True)
    class_ = Column(String)
    pop_estimate = Column(Integer)
    pop_margin = Column(Integer)
    urban_rural = Column(String)
    federal_average = Column(Float)
    state_average = Column(Float)
    local_average = Column(Float)