from sqlalchemy import ForeignKey, Integer, Column

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.helpers.columns import geo_id_column
from src.db.models.sqlalchemy.mixins import CreatedAtMixin


class LinkMunicipalityCensus(
    Base,
    CreatedAtMixin,
):

    __tablename__ = "link_municipality_census"

    municipality_id = Column(Integer, ForeignKey("municipality.id"), nullable=False)
    geo_id = geo_id_column()