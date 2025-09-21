from pydantic import BaseModel


class FindFilesInput(BaseModel):
    scrape_info_id: int
    municipality_name: str
    county_name: str
    year: int