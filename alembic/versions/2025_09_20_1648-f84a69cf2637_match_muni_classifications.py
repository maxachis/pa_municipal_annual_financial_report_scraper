"""Match Muni Classifications

Revision ID: f84a69cf2637
Revises: 08ae112d808e
Create Date: 2025-09-20 16:48:55.977743

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f84a69cf2637'
down_revision: Union[str, None] = '08ae112d808e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Meant to be run after src/dced_muni_classification/main.py,
    which populates the dced_muni_classification table
    """
    op.execute("""
        with
        db_county_muni as (
            select
                c.name as county,
                m.name as municipality,
                m.id as municipality_id
            from
                counties c
                join municipalities m
                     on c.id = m.county_id
            )
        , formatted_dced as (
            select
                upper(dced.county) as county,
                upper(
                        replace(
                                replace(dced.municipality, 'Borough', 'Boro'),
                                'Township', 'Twp'
                        )
                ) as municipality,
                dced.class
            from
                dced_muni_classification dced
            )
    insert into muni_classification (municipality_id, class)
    select
        db.municipality_id,
        dc.class
    from
        db_county_muni db
        inner join formatted_dced dc
             on db.county = dc.county and db.municipality = dc.municipality

    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
