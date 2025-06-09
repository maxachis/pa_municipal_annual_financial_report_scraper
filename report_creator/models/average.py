from typing import Optional

from pydantic import BaseModel


class AverageRow(BaseModel):
    """
    Represents a single row in the average sheet
    """
    county: str
    municipality: str
    federal_average: Optional[float] = None
    state_average: Optional[float] = None
    local_average: Optional[float] = None
