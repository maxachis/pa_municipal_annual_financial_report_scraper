from typing import Optional

from pydantic import BaseModel


class OptionInfo(BaseModel):
    """
    Data object storing data for value and label of an option
    """
    value: Optional[str] = None
    label: Optional[str] = None

    def report(self):
        print(f"Value: {self.value}, Label: {self.label}")
