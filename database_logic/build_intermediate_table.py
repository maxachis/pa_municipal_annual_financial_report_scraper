"""
This builds an intermediate table for manual inspection of the results
of fuzzy string matching.
"""

from database_logic.DatabaseManager import DatabaseManager
from database_logic.models import IntermediateTable

if __name__ == "__main__":
    dbm = DatabaseManager()
    dbm.wipe_table(IntermediateTable)
    dbm.build_intermediate_table()