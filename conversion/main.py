from db.client import DatabaseClient
from db.models.pydantic.cache_entry import CacheEntry
from scraper.JsonCache import JsonCache

if __name__ == "__main__":

    cache = JsonCache()
    cache.load_cache()
    cmys = cache.get_as_list_of_CMY()
    cache_entries = []
    for cmy in cmys:
        entry = cache._get_entry(cmy)
        cache_entry = CacheEntry(
            county_name=cmy.county,
            municipality_name=cmy.municipality,
            year=int(cmy.year),
            scraped=entry.scraped,
            scraper_error=entry.scraper_error,
            processed=entry.processed,
            process_error=entry.process_error
        )
        cache_entries.append(cache_entry)

    dbc = DatabaseClient()
    dbc.convert_state_to_db(cache_entries)