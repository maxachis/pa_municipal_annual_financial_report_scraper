"""Add total_revenue and code_category tables

Revision ID: 68d58fe4e5be
Revises: e1048b6d9630
Create Date: 2025-09-06 18:34:44.078395

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.db.alembic.helpers import id_column, created_at_column, updated_at_column, report_id_column

# revision identifiers, used by Alembic.
revision: str = '68d58fe4e5be'
down_revision: Union[str, None] = 'e1048b6d9630'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

OLD_CODES_NAME = 'codes_v2'
NEW_CODES_NAME = "codes"

OLD_JOINED_POP_DETAILS_NAME = 'joined_pop_details_v2'
NEW_JOINED_POP_DETAILS_NAME = "joined_pop_details"

TOTAL_REVENUE_TABLE_NAME = "total_revenue"
CODE_CATEGORY_TABLE_NAME = "code_category"

CODE_CATEGORY_ENUM = sa.Enum(
    'federal',
    'state',
    'local',
    name="code_category_enum"
)

def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table(OLD_CODES_NAME, NEW_CODES_NAME)
    op.rename_table(OLD_JOINED_POP_DETAILS_NAME, NEW_JOINED_POP_DETAILS_NAME)
    _add_total_revenue_table()
    _add_code_category_table()
    _populate_code_category_table()

def _add_total_revenue_table():
    op.create_table(
        TOTAL_REVENUE_TABLE_NAME,
        id_column(),
        created_at_column(),
        updated_at_column(),
        report_id_column(),
        sa.Column('total', sa.Float, nullable=False),
        sa.CheckConstraint('total >= 0', name='total_revenue_check')
    )

def _add_code_category_table():
    op.create_table(
        CODE_CATEGORY_TABLE_NAME,
        id_column(),
        created_at_column(),
        updated_at_column(),
        sa.Column(
            'code_id',
            sa.Integer,
            sa.ForeignKey('codes.id'),
            unique=True,
            nullable=False
        ),
        sa.Column('category', CODE_CATEGORY_ENUM, nullable=False),
    )

def _populate_code_category_table():
    # Federal
    op.execute(
        """
        INSERT INTO code_category (code_id, category)
        select
            id,
            'federal'::code_category_enum
        from
            codes
        where
            code in (
             '351.01',
             '351.02',
             '351.03',
             '351.04',
             '351.05',
             '351.06',
             '351.07',
             '351.08',
             '351.09',
             '351.1',
             '351.11',
             '351.12',
             '351.13',
             '351.XX'
            )
        """
    )
    # State
    op.execute(
        """
        INSERT INTO code_category (code_id, category)
        select
            id,
            'state'::code_category_enum
        from
            codes
        where
            code in (
                '354.01',
                '354.02',
                '354.03',
                '354.04',
                '345.05',
                '345.06',
                '345.07',
                '345.08',
                '354.09',
                '354.1',
                '354.11',
                '354.12',
                '354.13',
                '354.14',
                '354.15',
                '354.XX',
                '355.08'
            )
        """
    )
    # Local
    op.execute(
        """
        INSERT INTO code_category (code_id, category)
        select id,
               'local'::code_category_enum
        from codes
        where code in (
            '357.01',
            '357.02',
            '357.03',
            '357.XX'
            )
        """
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.rename_table(NEW_CODES_NAME, OLD_CODES_NAME)
    op.rename_table(NEW_JOINED_POP_DETAILS_NAME, OLD_JOINED_POP_DETAILS_NAME)
    op.drop_table(TOTAL_REVENUE_TABLE_NAME)
    op.drop_table(CODE_CATEGORY_TABLE_NAME)
