from sqlalchemy import Integer, Column
from sqlalchemy.orm import Mapped

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.helpers.columns import geo_id_column
from src.db.models.sqlalchemy.mixins import CreatedAtMixin, IDMixin


class CensusMunicipalityPopulation(
    Base,
    IDMixin,
    CreatedAtMixin,
):
    __tablename__ = "census_municipality_population"

    geo_id: Mapped[str] = geo_id_column()
    year = Column(Integer, nullable=False)
    population = Column(Integer, nullable=False)