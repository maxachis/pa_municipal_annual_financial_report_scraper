"""Add Urban Rural Classification

Revision ID: 63c32a548811
Revises: 74ff157a55b9
Create Date: 2025-09-13 18:27:45.195450

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '63c32a548811'
down_revision: Union[str, None] = '74ff157a55b9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


COUNTIES_TABLE_NAME = "counties"
COLUMN_NAME = "urban_rural"

def upgrade() -> None:
    """Upgrade schema."""
    _add_urban_rural_classification()
    _set_urban_rural_classification()

def _add_urban_rural_classification():
    op.add_column(
        "counties",
        sa.Column(COLUMN_NAME, sa.Enum(name='location_type_enum'), nullable=True)
    )

def _set_urban_rural_classification():
    op.execute(
        """
        UPDATE counties
        SET urban_rural = 
            CASE name
                WHEN 'INDIANA' THEN 'Rural'
                WHEN 'LAWRENCE' THEN 'Rural'
                WHEN 'BUTLER' THEN 'Rural'
                WHEN 'ALLEGHENY' THEN 'Urban'
                WHEN 'BEAVER' THEN 'Urban'
                WHEN 'WASHINGTON' THEN 'Rural'
                WHEN 'ARMSTRONG' THEN 'Rural'
                WHEN 'WESTMORELAND' THEN 'Urban'
                WHEN 'FAYETTE' THEN 'Rural'
                WHEN 'GREENE' THEN 'Rural'
                WHEN 'CAMBRIA' THEN 'Rural'
                WHEN 'SOMERSET' THEN 'Rural'
                ELSE '#N/A'
            END::location_type_enum
        """
    )

def _remove_urban_rural_classification():
    op.drop_column("counties", COLUMN_NAME)

def downgrade() -> None:
    """Downgrade schema."""
    _remove_urban_rural_classification()
