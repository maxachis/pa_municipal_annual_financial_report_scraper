from typing import Optional

from pydantic import BaseModel


class CMY(BaseModel):
    county: Optional[str] = None
    municipality: Optional[str] = None
    year: Optional[str] = None


class OptionInfo(BaseModel):
    value: Optional[str] = None
    label: Optional[str] = None

    def report(self):
        print(f"Value: {self.value}, Label: {self.label}")
