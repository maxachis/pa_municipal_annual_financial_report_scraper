"""Loads DCED Municipal Classification Into Database"""

import polars as pl
from sqlalchemy import create_engine, Engine

from src.db.constants import DB_CONNECTION_STRING


def main():
    dced_df: pl.DataFrame = pl.read_csv("data/muni_classification/municipalities.csv")

    dced_df = dced_df.rename(
        {
            "COUNTY": "county",
            "MUNICIPALITY": "municipality",
            "CLASS": "class"
        }
    )

    engine: Engine = create_engine(DB_CONNECTION_STRING)

    dced_df.write_database(
        connection=engine,
        table_name="dced_muni_classification",
        if_table_exists="append"
    )


if __name__ == "__main__":
    main()