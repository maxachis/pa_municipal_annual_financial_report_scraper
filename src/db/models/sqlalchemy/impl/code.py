from sqlalchemy import String, Column, UniqueConstraint

from src.db.models.sqlalchemy.base import StandardBase


class CodeV2(StandardBase):
    __tablename__ = 'codes'
    __table_args__ = (
        UniqueConstraint(
            'code',
            name='code_uq_code'
        ),
    )

    code = Column(String, primary_key=True)
    label = Column(String)
