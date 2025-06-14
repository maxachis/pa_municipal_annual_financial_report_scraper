from typing import Optional

from pydantic import BaseModel

from src.db.models.sqlalchemy.enums import LocationType


class AverageWithPopRow(BaseModel):
    county: str
    municipality: str
    federal_average: Optional[float] = None
    state_average: Optional[float] = None
    local_average: Optional[float] = None
    pop_estimate: int
    pop_margin: int
    urban_rural: LocationType
    class_: str
