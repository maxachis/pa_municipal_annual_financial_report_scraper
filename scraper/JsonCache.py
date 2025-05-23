"""
The JSONCache manages a cache of all data scraped and processed

The cache is stored in a JSON file.
The cache is a dictionary of county -> municipality -> year -> CacheObject
Each CacheObject represents the following:
- scraped: whether the entry has been scraped
- scraper_error: error message from the scraper, if any
- processed: whether the entry has been processed
- process_error: error message from the processor, if any

"""

import json
from pathlib import Path
from typing import Any, Optional, Annotated

from pydantic import BaseModel, Field

from config import YEARS
from scraper.data_objects import CMY
from util import project_path


class CacheObject(BaseModel):
    """
    A Pydantic model for a cache object.
    Though each individual cache object is a dictionary, this model is used to validate the data
    and ensure consistency in storage and access
    """
    scraped: Annotated[bool, Field(
        description="Whether the entry has been scraped",
        default=False
    )]
    scraper_error: Annotated[Optional[str], Field(
        description="Error message from the scraper",
        default=None
    )]
    processed: Annotated[bool, Field(
        description="Whether the entry has been processed",
        default=False
    )]
    process_error: Annotated[Optional[str], Field(
        description="Error message from the processor",
        default=None
    )]

class JsonCache:
    """
    A cache class for storing and retrieving data from a JSON file.
    """

    def __init__(self):
        self.path = project_path("cache.json")
        self.cache = {}

    def update_entry(self, cmy: CMY, data: Any):
        """Update an entry in the cache."""
        self.cache[cmy.county][cmy.municipality][cmy.year] = data
        self.save_cache()

    def all_municipalities_scraped(self, cmy: CMY) -> bool:
        d = self.cache.get(cmy.county, {}).get(cmy.municipality)
        if not d:
            return False
        for year in YEARS:
            if year not in d:
                return False
            cmy = CMY(county=cmy.county, municipality=cmy.municipality, year=year)
            cache_object = self._get_entry(cmy)
            if not cache_object.scraped:
                return False
        return True

    def _get_entry(self, cmy: CMY) -> CacheObject:
        """Retrieve an entry from the cache."""
        raw_data = self.cache.get(cmy.county, {}).get(cmy.municipality, {}).get(cmy.year, {})
        return CacheObject(**raw_data)

    def save_cache(self):
        """Save the cache to a JSON file."""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=4)

    def load_cache(self):
        """Load the cache from a JSON file."""
        path = Path(self.path)
        if path.exists():
            with open(self.path, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def add_scraper_error(self, cmy: CMY, error: str):
        cache_object = self._get_entry(cmy)
        cache_object.scraper_error = error
        self._update_entry(cmy, cache_object)

    def add_process_error(self, cmy: CMY, error: str):
        cache_object = self._get_entry(cmy)
        cache_object.process_error = error
        self._update_entry(cmy, cache_object)

    def mark_as_scraped(self, cmy: CMY):
        cache_object = self._get_entry(cmy)
        cache_object.scraped = True
        self._update_entry(cmy, cache_object)

    def mark_as_processed(self, cmy: CMY):
        cache_object = self._get_entry(cmy)
        cache_object.processed = True
        self._update_entry(cmy, cache_object)

    def _update_entry(self, cmy: CMY, cache_object: CacheObject):
        if cmy.county not in self.cache:
            self.cache[cmy.county] = {}
        if cmy.municipality not in self.cache[cmy.county]:
            self.cache[cmy.county][cmy.municipality] = {}
        if cmy.year not in self.cache[cmy.county][cmy.municipality]:
            self.cache[cmy.county][cmy.municipality][cmy.year] = {}
        self.cache[cmy.county][cmy.municipality][cmy.year] = cache_object.model_dump()
        self.save_cache()

    def is_scraped(self, cmy: CMY) -> bool:
        result = self._get_entry(cmy)
        return result.scraped

    def has_scraper_error(self, cmy: CMY, error_substring: str) -> bool:
        result = self._get_entry(cmy)
        if not result.scraper_error:
            return False
        return error_substring in result.scraper_error

    def has_timeout_error(self, cmy: CMY) -> bool:
        return self.has_scraper_error(cmy, "Timeout")

    def get_as_list_of_CMY(self) -> list[CMY]:
        """
        Get a list of CMY objects from the cache
        :return:
        """
        cmy_list = []
        for county in self.cache.keys():
            for municipality in self.cache[county].keys():
                for year in self.cache[county][municipality].keys():
                    cmy = CMY(
                        county=county,
                        municipality=municipality,
                        year=year
                    )
                    entry = self._get_entry(cmy)
                    if not entry.scraped:
                        continue
                    cmy_list.append(cmy)
        return cmy_list

    def county_reset(self, county: str):
        self.cache[county] = {}
        self.save_cache()

# Uncomment to reset county of choice
# if __name__ == "__main__":

#     cache = JsonCache()
#     cache.load_cache()
#     cache.county_reset("WESTMORELAND")
#     cache.save_cache()
