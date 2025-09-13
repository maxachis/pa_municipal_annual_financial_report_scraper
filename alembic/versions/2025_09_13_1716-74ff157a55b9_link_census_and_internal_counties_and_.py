"""Link Census and Internal Counties and Municipalities

Revision ID: 74ff157a55b9
Revises: 0046af7dea7f
Create Date: 2025-09-13 17:16:52.337746

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '74ff157a55b9'
down_revision: Union[str, None] = '0046af7dea7f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    _add_pg_trgm()
    _link_county_census()
    _link_municipality_census()

def downgrade() -> None:
    """Downgrade schema."""
    _remove_pg_trgm()
    _clear_link_county_census()
    _clear_link_municipality_census()

def _link_county_census():
    op.execute("""
        with
        census_county_parsed as (
            select
                id,
                upper(replace(name, 'County', '')) as name
            from census_county
        )
        INSERT INTO link_county_census (county_id, census_county_id)
        select
            c.id as county_id,
            ccp.id census_county_id
        from census_county_parsed ccp
        inner join counties c on similarity(ccp.name, c.name) = 1
    
    """)

def _link_municipality_census():
    op.execute("""
            with
            internal_county_municipalities as (
                select
                    counties.id as county_id,
                    municipalities.id as municipality_id,
                    replace(
                            replace(
                                replace(
                                    municipalities.name, ' TWP', ' TOWNSHIP'
                                ), ' BORO', ' BOROUGH'
                    ), 'MT ', 'MOUNT ') as municipality_name
                from
                    counties
                    join
                        municipalities
                        on municipalities.county_id = counties.id
                )
            , census_county_municipalities as (
                select
                    census_county.id as county_id,
                    census_municipality.geo_id as municipality_id,
                    -- Three instances of municipalities with the word municipality in the name
                    -- (Murrysville, Bethel Park, Monroeville) are all DCED classified as Boroughs
                    
                    -- Remove ' in O'Hara to match internal municipality name
                    
                    -- Latrobe Borough is misclassified in the census as Latrobe City
                    upper(replace(replace(replace(
                            census_municipality.name, 'municipality', 'borough'
                          ), 'O''Hara', 'OHARA'), 'Latrobe city', 'Latrobe borough')) as municipality_name
                from
                    census_county
                    join
                        census_municipality
                        on census_municipality.census_county_id = census_county.id
                )
        INSERT INTO link_municipality_census (municipality_id, geo_id)
        select
            icm.municipality_id,
            ccm.municipality_id
        from
            internal_county_municipalities icm
                join link_county_census lcm on lcm.county_id = icm.county_id
            join census_county_municipalities ccm
                 on lcm.census_county_id = ccm.county_id
        where similarity(icm.municipality_name, ccm.municipality_name) = 1
    """)

def _clear_link_county_census():
    op.execute("DELETE FROM link_county_census")

def _clear_link_municipality_census():
    op.execute("DELETE FROM link_municipality_census")

def _add_pg_trgm():
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

def _remove_pg_trgm():
    op.execute("DROP EXTENSION IF EXISTS pg_trgm")
