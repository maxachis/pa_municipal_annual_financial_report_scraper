from sqlalchemy import Column, String

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.mixins import CreatedAtMixin, IDMixin


class CensusCounty(
    Base,
    IDMixin,
    CreatedAtMixin
):
    __tablename__ = "census_county"

    name = Column(String, nullable=False)
