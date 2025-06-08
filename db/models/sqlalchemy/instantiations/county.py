from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.orm import relationship

from db.models.sqlalchemy.base import StandardBase


class County(StandardBase):
    __tablename__ = "counties"
    __table_args__ = (
        UniqueConstraint(
            "name",
            name="county_uq_name"
        ),
    )
    name = Column(String)

    municipalities = relationship(
        "Municipality",
        back_populates="county"
    )

    reports = relationship(
        "AnnualReport",
        back_populates="county"
    )
