from enum import Enum as PyEnum, EnumType
from typing import cast

from sqlalchemy import Enum as SAEnum
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
