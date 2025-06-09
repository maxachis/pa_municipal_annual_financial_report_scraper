"""Add On Delete Cascades

Revision ID: e1048b6d9630
Revises: dd06379e33bf
Create Date: 2025-06-08 21:46:45.308514

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1048b6d9630'
down_revision: Union[str, None] = 'dd06379e33bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    for foreign_key, table in [
        ('scrape_errors_report_id_fkey', 'scrape_errors'),
        ('scrape_info_report_id_fkey', 'scrape_info'),
        ('process_errors_report_id_fkey', 'process_errors'),
        ('process_info_report_id_fkey', 'process_info'),
        ('report_details_report_id_fkey', 'report_details')
    ]:
        op.drop_constraint(foreign_key, table)
        op.create_foreign_key(
            foreign_key,
            source_table=table,
            referent_table='annual_reports',
            local_cols=['report_id'],
            remote_cols=['id'],
            ondelete='CASCADE'
        )


def downgrade() -> None:
    """Downgrade schema."""
    pass
