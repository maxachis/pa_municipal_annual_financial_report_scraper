"""Create census data tables

Revision ID: 0046af7dea7f
Revises: 68d58fe4e5be
Create Date: 2025-09-13 15:32:23.511497

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from src.db.alembic.helpers import id_column, county_id_column, created_at_column, municipality_id_column

# revision identifiers, used by Alembic.
revision: str = '0046af7dea7f'
down_revision: Union[str, None] = '68d58fe4e5be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

LINK_COUNTY_CENSUS_TABLE_NAME = "link_county_census"
LINK_MUNICIPALITY_CENSUS_TABLE_NAME = "link_municipality_census"
CENSUS_COUNTY_TABLE_NAME = "census_county"
CENSUS_MUNICIPALITY_TABLE_NAME = "census_municipality"
CENSUS_MUNICIPALITY_POPULATION_TABLE_NAME = "census_municipality_population"

def upgrade() -> None:
    """Upgrade schema."""
    _create_census_county_table()
    _create_census_municipality_table()
    _create_census_municipality_population_table()
    _create_link_county_census_table()
    _create_link_municipality_census_table()

def _create_census_municipality_population_table():
    op.create_table(
        CENSUS_MUNICIPALITY_POPULATION_TABLE_NAME,
        id_column(),
        sa.Column(
            "geo_id",
            sa.String,
            sa.ForeignKey(f"{CENSUS_MUNICIPALITY_TABLE_NAME}.geo_id"),
            nullable=False
        ),
        sa.Column(
            "year",
            sa.Integer,
            nullable=False
        ),
        sa.Column(
            "population",
            sa.Integer,
            nullable=False
        ),
        created_at_column(),
        sa.UniqueConstraint(
            "geo_id", "year",
            name="census_municipality_population_uq_census_municipality"
        ),
        sa.CheckConstraint(
            "year BETWEEN 2015 AND 2024",
            name="census_municipality_population_cc_year"
        ),
        sa.CheckConstraint(
            "population >= 0",
            name="census_municipality_population_cc_population"
        )
    )

def _create_link_county_census_table():
    op.create_table(
        LINK_COUNTY_CENSUS_TABLE_NAME,
        county_id_column(),
        sa.Column(
            "census_county_id",
            sa.Integer,
            sa.ForeignKey(f"{CENSUS_COUNTY_TABLE_NAME}.id"),
            nullable=False
        ),
        created_at_column(),
        # Each ID should only appear once
        sa.UniqueConstraint(
            "county_id",
            name="link_county_census_uq_county"
        ),
        sa.UniqueConstraint(
            "census_county_id",
            name="link_county_census_uq_census_county"
        )
    )

def _create_link_municipality_census_table():
    op.create_table(
        LINK_MUNICIPALITY_CENSUS_TABLE_NAME,
        municipality_id_column(),
        sa.Column(
            "geo_id",
            sa.String,
            sa.ForeignKey(f"{CENSUS_MUNICIPALITY_TABLE_NAME}.geo_id"),
            nullable=False
        ),
        created_at_column(),
        # Each ID should only appear once
        sa.UniqueConstraint(
            "municipality_id",
            name="link_municipality_census_uq_municipality_id"
        ),
        sa.UniqueConstraint(
            "geo_id",
            name="link_municipality_census_uq_geo_id"
        )
    )

def _create_census_county_table():
    op.create_table(
        CENSUS_COUNTY_TABLE_NAME,
        id_column(autoincrement=False),
        sa.Column(
            "name",
            sa.String,
            nullable=False,
        ),
        created_at_column(),
        sa.UniqueConstraint("name", name="census_county_uq_name")
    )

def _create_census_municipality_table():
    op.create_table(
        CENSUS_MUNICIPALITY_TABLE_NAME,
        sa.Column(
            "census_county_id",
            sa.Integer,
            sa.ForeignKey(f"{CENSUS_COUNTY_TABLE_NAME}.id"),
            nullable=False
        ),
        sa.Column(
            "name",
            sa.String,
            nullable=False,
        ),
        sa.Column(
            "geo_id",
            sa.String,
            nullable=False,
            primary_key=True
        ),
        created_at_column(),
        sa.UniqueConstraint(
            "name",
            "census_county_id",
            name="census_municipality_uq_name"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(LINK_COUNTY_CENSUS_TABLE_NAME)
    op.drop_table(LINK_MUNICIPALITY_CENSUS_TABLE_NAME)
    op.drop_table(CENSUS_MUNICIPALITY_POPULATION_TABLE_NAME)
    op.drop_table(CENSUS_MUNICIPALITY_TABLE_NAME)
    op.drop_table(CENSUS_COUNTY_TABLE_NAME)