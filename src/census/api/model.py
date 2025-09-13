from pydantic import BaseModel


class CensusData(BaseModel):
    geo_id: str
    name: str
    county_id: int
    municipality_id: int
    population: int