from pydantic import BaseModel

from db.models.sqlalchemy.enums import LocationType


class PopRow(BaseModel):
    geo_id: str
    county: str
    municipality: str
    class_: str
    pop_estimate: int
    pop_margin: int
    location_type: LocationType