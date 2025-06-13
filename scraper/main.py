"""
Main function for scraping municipal annual financial reports
"""

import asyncio

from playwright.async_api import async_playwright

from JsonCache import JsonCache
from db.client import DatabaseClient
from scraper.core import Scraper
from scraper.helpers import load_page


async def main():
    async with async_playwright() as p:
        page = await load_page(p)
        scraper = Scraper(
            db_client=DatabaseClient(),
            page=page
        )
        await scraper.run()

if __name__ == "__main__":
    max_additional_attempts = 0
    for i in range(max_additional_attempts):
        try:
            asyncio.run(main())
            exit(0)
        except Exception as e:
            print(f"Error: {e}. Restarting ({max_additional_attempts - i} attempts left).")
    asyncio.run(main())


