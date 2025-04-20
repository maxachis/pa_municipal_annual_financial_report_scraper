from typing import Optional

from pydantic import BaseModel


class CMYBreakdownRow(BaseModel):
    """
    Represents a single row in the breakdown sheet
    """
    county: str
    municipality: str
    year: str
    federal_amt: int
    state_amt: int
    local_amt: int

    def get_total(self):
        return self.federal_amt + self.state_amt + self.local_amt

class AverageRow(BaseModel):
    """
    Represents a single row in the average sheet
    """
    county: str
    municipality: str
    federal_average: Optional[float] = None
    state_average: Optional[float] = None
    local_average: Optional[float] = None

class AverageWithPopRow(AverageRow):
    pop_estimate: int
    pop_margin: int
    urban_rural: str
    class_: str