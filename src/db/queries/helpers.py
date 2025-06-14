from sqlalchemy import or_

from src.config import FEDERAL_PREFIX, STATE_CODES, STATE_PREFIX, LOCAL_PREFIX
from src.db.models.sqlalchemy.instantiations import CodeV2


def get_federal_conditions():
    return CodeV2.code.like(f"{FEDERAL_PREFIX}%")

def get_state_conditions():
    return or_(
        CodeV2.code.in_(STATE_CODES),
        CodeV2.code.like(f"{STATE_PREFIX}%")
    )

def get_local_conditions():
    return CodeV2.code.like(f"{LOCAL_PREFIX}%")