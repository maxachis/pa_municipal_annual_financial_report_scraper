from sqlalchemy import UniqueConstraint, Column, String
from sqlalchemy.orm import relationship

from db.models.sqlalchemy.base import StandardBase
from db.models.sqlalchemy.mixins import CountyMixin


class Municipality(
    StandardBase,
    CountyMixin
):
    __tablename__ = "municipalities"
    __table_args__ = (
        UniqueConstraint(
            "county_id",
            name="municipality_uq_county_name"
        ),
    )
    name = Column(String, unique=True)

    reports = relationship(
        "AnnualReport",
        back_populates="municipality"
    )
