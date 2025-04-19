from pydantic import BaseModel

class PopRow(BaseModel):
    geo_id: str
    county: str
    municipality: str
    class_: str
    pop_estimate: int
    pop_margin: int
    urban_rural: str