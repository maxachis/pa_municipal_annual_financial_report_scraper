"""Create dced_muni_classification

Revision ID: 08ae112d808e
Revises: 80177543515f
Create Date: 2025-09-20 16:30:54.336138

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.db.alembic.helpers import municipality_id_column, created_at_column

# revision identifiers, used by Alembic.
revision: str = '08ae112d808e'
down_revision: Union[str, None] = '80177543515f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "dced_muni_classification",
        sa.Column("county", sa.String, primary_key=True),
        sa.Column("municipality", sa.String, primary_key=True),
        sa.Column("class", sa.String(255), nullable=False),

    )

    op.create_table(
        "muni_classification",
        municipality_id_column(),
        sa.Column("class", sa.String(255), nullable=False),
        created_at_column(),
        sa.PrimaryKeyConstraint(
            "municipality_id",
            name="muni_classification_pk_municipality"
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("dced_muni_classification")
    op.drop_table("muni_classification")
