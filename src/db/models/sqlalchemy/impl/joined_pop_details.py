from sqlalchemy import Integer, String, Column, UniqueConstraint
from sqlalchemy.orm import Mapped

from src.db.models.sqlalchemy.base import StandardBase
from src.db.models.sqlalchemy.enums import LocationType
from src.db.models.sqlalchemy.helpers.columns import enum_column
from src.db.models.sqlalchemy.mixins import MunicipalityMixin, CountyMixin


class JoinedPopDetailsV2(
    StandardBase,
    CountyMixin,
    MunicipalityMixin
):
    __tablename__ = "joined_pop_details_v2"
    __table_args__ = (
        UniqueConstraint(
            "geo_id",
            name="joined_pop_details_v2_uq_geo_id"
        ),
        UniqueConstraint(
            "county_id",
            "municipality_id",
            name="joined_pop_details_v2_uq_county_municipality"
        )
    )

    geo_id = Column(String, primary_key=True)
    class_ = Column('class', String, key="class_")
    pop_estimate = Column(Integer)
    pop_margin = Column(Integer)
    location_type: Mapped[LocationType] = enum_column(
        enum_=LocationType,
        name="location_type_enum"
    )