from pydantic import BaseModel


class CMYBreakdownRow(BaseModel):
    county: str
    municipality: str
    year: str
    federal_amt: int
    state_amt: int
    local_amt: int

    def get_total(self):
        return self.federal_amt + self.state_amt + self.local_amt
