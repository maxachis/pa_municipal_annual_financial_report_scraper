"""
This builds an intermediate table for manual inspection of the results
of fuzzy string matching.
"""

from db.client import DatabaseClient
from db.models.sqlalchemy.models_old import IntermediateTable

if __name__ == "__main__":
    dbm = DatabaseClient()
    dbm.wipe_table(IntermediateTable)
    dbm.build_intermediate_table()