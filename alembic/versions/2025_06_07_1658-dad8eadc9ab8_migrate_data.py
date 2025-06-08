"""Migrate data

Revision ID: dad8eadc9ab8
Revises: 587d9ec1a28d
Create Date: 2025-06-07 16:58:40.494647

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dad8eadc9ab8'
down_revision: Union[str, None] = '587d9ec1a28d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    INSERT INTO codes_v2 (code, label)
    SELECT code, label
    FROM codes
    """)

    op.execute("""
    INSERT INTO
    report_details (report_id, code_id, total)
    SELECT
        ar.id,
        codes_v2.id,
        afrd.total
        FROM
            annual_reports ar
            JOIN COUNTIES c
                ON c.id = ar.county_id
            JOIN MUNICIPALITIES m
                ON m.id = ar.municipality_id
            JOIN annual_financial_report_details afrd
                ON
                afrd.county = c.name
                    AND afrd.municipality = m.name
                    AND afrd.year::int = ar.year
            JOIN codes_v2
                ON afrd.code = codes_v2.code

    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
