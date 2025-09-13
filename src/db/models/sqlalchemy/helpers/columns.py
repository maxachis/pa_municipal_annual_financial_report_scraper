from datetime import datetime
from enum import Enum as PyEnum, EnumType
from typing import cast

from sqlalchemy import Enum as SAEnum, Column, Integer, DateTime, func, ForeignKey, String
from sqlalchemy.orm import mapped_column, MappedColumn


def enum_column(
    enum_: EnumType,
    name: str
) -> MappedColumn[PyEnum]:
    return mapped_column(
        SAEnum(
            cast(type[PyEnum], enum_),
            name=name,
            native_enum=True,
            validate_strings=True,
            values_callable=lambda x: [e.value for e in x]
        )
    )

def id_column() -> Column[int]:
    return Column(Integer, primary_key=True, index=True)

def created_at_column() -> Column[datetime]:
    return Column(
        DateTime,
        default=func.now(),
        server_default=func.now(),
    )

def census_county_id_column() -> Column[int]:
    return Column(Integer, ForeignKey("census_county.id"), nullable=False)

def geo_id_column() -> Column[str]:
    return Column(String, ForeignKey("census_municipality.geo_id"), nullable=False)