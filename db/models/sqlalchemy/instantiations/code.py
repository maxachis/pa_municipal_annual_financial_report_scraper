from sqlalchemy import String, Column

from db.models.sqlalchemy.base import StandardBase


class CodeV2(StandardBase):
    __tablename__ = 'codes_v2'

    code = Column(String, primary_key=True)
    label = Column(String)
