import json
from pathlib import Path
from typing import Any

from constants import YEARS
from data_objects import CMY


class JsonCache:
    """
    A cache class for storing and retrieving data from a JSON file.
    """

    def __init__(self, filename: str):
        self.filename = filename
        self.cache = {}

    def add_entry(self, cmy: CMY, data: Any):
        """Add an entry to the cache."""
        self.cache.setdefault(cmy.county, {}).setdefault(cmy.municipality, {})[cmy.year] = data
        self.save_cache()

    def has_all_municipality_entries(self, cmy: CMY) -> bool:
        d = self.cache.get(cmy.county, {}).get(cmy.municipality)
        if not d:
            return False
        return len(d.keys()) == len(YEARS)

    def get_entry(self, cmy: CMY) -> Any:
        """Retrieve an entry from the cache."""
        return self.cache.get(cmy.county, {}).get(cmy.municipality, {}).get(cmy.year)

    def save_cache(self):
        """Save the cache to a JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.cache, f, ensure_ascii=False, indent=4)

    def load_cache(self):
        """Load the cache from a JSON file."""
        path = Path(self.filename)
        if path.exists():
            with open(self.filename, 'r', encoding='utf-8') as f:
                self.cache = json.load(f)
        else:
            self.cache = {}
