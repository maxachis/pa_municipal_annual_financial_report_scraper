from pydantic import BaseModel


class CMYBreakdownRow(BaseModel):
    """
    Represents a single row in the breakdown sheet
    """
    county: str
    municipality: str
    year: int
    federal_amt: int
    state_amt: int
    local_amt: int

    def get_total(self):
        return self.federal_amt + self.state_amt + self.local_amt
