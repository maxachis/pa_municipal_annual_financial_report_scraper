from sqlalchemy import Column, Integer, ForeignKey

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.helpers.columns import census_county_id_column
from src.db.models.sqlalchemy.mixins import CreatedAtMixin


class LinkCountyCensus(
    Base,
    CreatedAtMixin
):

    __tablename__ = "link_county_census"

    county_id = Column(Integer, ForeignKey("county.id"), nullable=False)
    census_county_id = census_county_id_column()