from sqlalchemy import Column, String, Integer, Enum
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

