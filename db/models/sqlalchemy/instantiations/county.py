from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.models.sqlalchemy.base import StandardBase


class County(StandardBase):
    __tablename__ = "counties"
    name = Column(String, unique=True)

    municipalities = relationship(
        "Municipality",
        back_populates="county"
    )

    reports = relationship(
        "AnnualReport",
        back_populates="county"
    )
