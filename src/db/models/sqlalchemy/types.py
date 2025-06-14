from enum import Enum
from typing import TypeVar

from sqlalchemy import TypeDecorator
from sqlalchemy.dialects.postgresql import ENUM

EnumType = TypeVar("EnumType", bound=Enum)


class EnumValue(TypeDecorator):
    impl = ENUM

    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return value.value

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class(value)