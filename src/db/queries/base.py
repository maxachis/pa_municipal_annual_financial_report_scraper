from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session

from src.db.helpers import compile_query


class QueryBuilder(ABC):

    @staticmethod
    def compile_query(query):
        return compile_query(query)

    @abstractmethod
    def run(self, session: Session) -> Any:
        ...
