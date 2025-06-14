"""Add new normalized tables

Revision ID: 587d9ec1a28d
Revises: 
Create Date: 2025-06-07 14:52:07.736531

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy import UniqueConstraint, ForeignKey

from src.db.alembic import county_id_column, municipality_id_column, standard_columns, report_id_column

# revision identifiers, used by Alembic.
revision: str = '587d9ec1a28d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

ANNUAL_REPORTS_TABLE_NAME = 'annual_reports'
MUNICIPALITIES_TABLE_NAME = 'municipalities'
COUNTIES_TABLE_NAME = 'counties'
CODE_V2_TABLE_NAME = 'codes_v2'
JOINED_POP_DETAILS_V2_TABLE_NAME = 'joined_pop_details_v2'
PROCESS_ERRORS_TABLE_NAME = 'process_errors'
SCRAPE_ERRORS_TABLE_NAME = 'scrape_errors'
PROCESS_INFO_TABLE_NAME = 'process_info'
SCRAPE_INFO_TABLE_NAME = 'scrape_info'
REPORT_DETAILS_TABLE_NAME = 'report_details'

LOCATION_TYPE_ENUM_NAME = 'location_type_enum'

location_type_enum = sa.Enum(
    'Urban',
    'Rural',
    '#N/A',
    name=LOCATION_TYPE_ENUM_NAME
)

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        COUNTIES_TABLE_NAME,
        *standard_columns(),
        sa.Column('name', sa.String, nullable=False),
        UniqueConstraint(
            'name',
            name='county_uq_name'
        )
    )

    op.create_table(
        MUNICIPALITIES_TABLE_NAME,
        *standard_columns(),
        county_id_column(),
        sa.Column('name', sa.String, nullable=False),
        UniqueConstraint(
            'name',
            'county_id',
            name='municipality_uq_county_name'
        )
    )

    op.create_table(
        ANNUAL_REPORTS_TABLE_NAME,
        *standard_columns(),
        county_id_column(),
        municipality_id_column(),
        sa.Column('year', sa.Integer, nullable=False),
        UniqueConstraint(
            'year',
            'county_id',
            'municipality_id',
            name='annual_report_uq_county_municipality_year'
        )
    )

    op.create_table(
        CODE_V2_TABLE_NAME,
        *standard_columns(),
        sa.Column('code', sa.String, nullable=False),
        sa.Column('label', sa.String, nullable=False),
        UniqueConstraint(
            'code',
            name='code_uq_code'
        )
    )

    op.create_table(
        JOINED_POP_DETAILS_V2_TABLE_NAME,
        *standard_columns(),
        county_id_column(),
        municipality_id_column(),
        sa.Column('geo_id', sa.String, nullable=False),
        sa.Column('class', sa.String, nullable=False),
        sa.Column('pop_estimate', sa.Integer, nullable=False),
        sa.Column('pop_margin', sa.Integer, nullable=False),
        sa.Column('location_type', location_type_enum, nullable=False),
        UniqueConstraint(
            "geo_id",
            name="joined_pop_details_v2_uq_geo_id"
        ),
        UniqueConstraint(
            "county_id",
            "municipality_id",
            name="joined_pop_details_v2_uq_county_municipality"
        )
    )

    op.create_table(
        REPORT_DETAILS_TABLE_NAME,
        *standard_columns(),
        report_id_column(),
        sa.Column(
            'code_id',
            sa.Integer,
            ForeignKey('codes_v2.id'),
            nullable=False),
        sa.Column('total', sa.Integer, nullable=False),
        UniqueConstraint(
            "report_id",
            "code_id",
            name="report_details_uq_report"
        ),
    )

    op.create_table(
        PROCESS_ERRORS_TABLE_NAME,
        *standard_columns(),
        report_id_column(),
        sa.Column('message', sa.String, nullable=False),
        UniqueConstraint(
            "report_id",
            name="process_error_uq_report"
        ),
    )

    op.create_table(
        SCRAPE_ERRORS_TABLE_NAME,
        *standard_columns(),
        report_id_column(),
        sa.Column('message', sa.String, nullable=False),
        UniqueConstraint(
            "report_id",
            name="scrape_error_uq_report_id"
        ),
    )

    op.create_table(
        PROCESS_INFO_TABLE_NAME,
        *standard_columns(),
        report_id_column(),
        UniqueConstraint(
            "report_id",
            name="process_info_uq_report"
        )
    )

    op.create_table(
        SCRAPE_INFO_TABLE_NAME,
        *standard_columns(),
        report_id_column(),
        sa.Column('filename', sa.String, nullable=True),
        UniqueConstraint(
            "report_id",
            name="scrape_info_uq_report"
        ),
        UniqueConstraint(
            "filename",
            name="scrape_info_uq_filename"
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(PROCESS_ERRORS_TABLE_NAME)
    op.drop_table(SCRAPE_ERRORS_TABLE_NAME)
    op.drop_table(PROCESS_INFO_TABLE_NAME)
    op.drop_table(SCRAPE_INFO_TABLE_NAME)
    op.drop_table(REPORT_DETAILS_TABLE_NAME)
    op.drop_table(JOINED_POP_DETAILS_V2_TABLE_NAME)
    op.drop_table(ANNUAL_REPORTS_TABLE_NAME)
    op.drop_table(MUNICIPALITIES_TABLE_NAME)
    op.drop_table(COUNTIES_TABLE_NAME)
    op.drop_table(CODE_V2_TABLE_NAME)

    location_type_enum.drop(op.get_bind())
