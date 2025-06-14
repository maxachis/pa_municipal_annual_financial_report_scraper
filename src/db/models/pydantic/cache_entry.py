from typing import Optional

from pydantic import BaseModel


class CacheEntry(BaseModel):
    county_name: str
    municipality_name: str
    year: int
    scraped: bool
    scraper_error: Optional[str] = None
    processed: bool
    process_error: Optional[str] = None
