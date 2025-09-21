"""Create grant total views

Revision ID: 80177543515f
Revises: 63c32a548811
Create Date: 2025-09-20 09:39:11.790500

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80177543515f'
down_revision: Union[str, None] = '63c32a548811'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
    CREATE VIEW FEDERAL_TOTAL_PER_REPORT as
    select
        rd.report_id,
        sum(rd.total) as report_total
    from report_details rd
    join codes c on c.id = rd.code_id
    where c.code like '351%'
    group by rd.report_id
    """)

    op.execute("""
    CREATE VIEW STATE_TOTAL_PER_REPORT as
    select
        rd.report_id,
        sum(rd.total) as report_total
    from report_details rd
         join codes c on c.id = rd.code_id
    where c.code like '354%'
    group by rd.report_id
    """)

    op.execute("""
    CREATE VIEW LOCAL_TOTAL_PER_REPORT as
    select
        rd.report_id,
        sum(rd.total) as report_total
    from report_details rd
         join codes c on c.id = rd.code_id
    where c.code like '357%'
    group by rd.report_id
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
    DROP VIEW FEDERAL_TOTAL_PER_REPORT
    """)

    op.execute("""
    DROP VIEW STATE_TOTAL_PER_REPORT
    """)

    op.execute("""
    DROP VIEW LOCAL_TOTAL_PER_REPORT
        """)
