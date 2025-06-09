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

from typing import Any

from scraper.models.cmy import CMY


class JsonCache:
    """
    A cache class for storing and retrieving data from a JSON file.
    """

    def __init__(self):
        raise NotImplementedError

    def update_entry(self, cmy: CMY, data: Any):
        """Update an entry in the cache."""
        raise NotImplementedError

    def all_municipalities_scraped(self, cmy: CMY) -> bool:
        raise NotImplementedError

    def _get_entry(self, cmy: CMY) -> Any:
        """Retrieve an entry from the cache."""
        raise NotImplementedError

    def save_cache(self):
        """Save the cache to a JSON file."""
        raise NotImplementedError

    def load_cache(self):
        """Load the cache from a JSON file."""
        raise NotImplementedError

    def add_scraper_error(self, cmy: CMY, error: str):
        raise NotImplementedError

    def add_process_error(self, cmy: CMY, error: str):
        raise NotImplementedError

    def mark_as_scraped(self, cmy: CMY):
        raise NotImplementedError

    def mark_as_processed(self, cmy: CMY):
        raise NotImplementedError

    def is_scraped(self, cmy: CMY) -> bool:
        raise NotImplementedError

    def has_scraper_error(self, cmy: CMY, error_substring: str) -> bool:
        raise NotImplementedError

    def has_timeout_error(self, cmy: CMY) -> bool:
        return self.has_scraper_error(cmy, "Timeout")

    def get_as_list_of_CMY(self) -> list[CMY]:
        """
        Get a list of CMY objects from the cache
        :return:
        """
        raise NotImplementedError

