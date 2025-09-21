from typing import ClassVar

from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, event
from sqlalchemy.orm import relationship, declared_attr, Mapped


class CountyMixin:
    county_id = Column(Integer, ForeignKey("counties.id"))

    @declared_attr
    def county(cls) -> Mapped["County"]:
        return relationship("County")


class MunicipalityMixin:
    municipality_id = Column(Integer, ForeignKey("municipalities.id"))


    @declared_attr
    def municipality(self) -> Mapped["Municipality"]:
        return relationship("Municipality")

class AnnualReportMixin:
    report_id = Column(Integer, ForeignKey("annual_reports.id"))

    @declared_attr
    def report(self) -> Mapped["AnnualReport"]:
        return relationship("AnnualReport")

class IDMixin:
    id = Column(Integer, primary_key=True, index=True)

class CreatedAtMixin:
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now()
    )

class ViewMixin:
    """Attach to any mapped class that represents a DB view."""
    __is_view__: ClassVar[bool] = True

    @classmethod
    def __declare_last__(cls) -> None:
        # Block writes on this mapped class
        for evt in ("before_insert", "before_update", "before_delete"):
            event.listen(cls, evt, cls._block_write)

    @staticmethod
    def _block_write(mapper, connection, target):
        raise ValueError(f"{type(target).__name__} is a read-only view.")
