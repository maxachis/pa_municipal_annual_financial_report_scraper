"""Add invalid municipalities

Revision ID: 9cf8cc9b3caa
Revises: f84a69cf2637
Create Date: 2025-09-27 09:32:45.598471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cf8cc9b3caa'
down_revision: Union[str, None] = 'f84a69cf2637'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "flag_invalid_municipalities",
        sa.Column(
            "municipality_id",
            sa.Integer,
            sa.ForeignKey("municipalities.id"),
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("invalid_municipalities")
