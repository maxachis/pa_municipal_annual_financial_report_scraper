"""
This builds an intermediate table for manual inspection of the results
of fuzzy string matching.
"""

from db.DatabaseManager import DatabaseManager
from db.models.sqlalchemy import IntermediateTable

if __name__ == "__main__":
    dbm = DatabaseManager()
    dbm.wipe_table(IntermediateTable)
    dbm.build_intermediate_table()