from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.orm import Session


class QueryBuilder(ABC):

    @abstractmethod
    def run(self, session: Session) -> Any:
        ...
