from sqlalchemy import Column, String, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped

from src.db.models.sqlalchemy.base import Base
from src.db.models.sqlalchemy.helpers.columns import census_county_id_column
from src.db.models.sqlalchemy.mixins import CreatedAtMixin


class CensusMunicipality(
    Base,
    CreatedAtMixin,
):
    __tablename__ = "census_municipality"
    __table_args__ = (
        PrimaryKeyConstraint(
            "geo_id",
            name="census_municipality_pk_geo_id"
        ),
    )

    census_county_id: Mapped[int] = census_county_id_column()
    name = Column(String, nullable=False)
    geo_id = Column(String, nullable=False)

