"""Remove old tables

Revision ID: dd06379e33bf
Revises: dad8eadc9ab8
Create Date: 2025-06-07 20:23:51.519271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd06379e33bf'
down_revision: Union[str, None] = 'dad8eadc9ab8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_table('codes')
    op.drop_table('annual_financial_report_details')
    op.drop_table('joined_pop_details')
    op.drop_table('intermediate_table')


def downgrade() -> None:
    """Downgrade schema."""
    raise NotImplementedError
