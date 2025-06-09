from typing import Optional

from pydantic import BaseModel


class CMY(BaseModel):
    """
    Data object storing data for County, Municipality, Year
    """
    county: Optional[str] = None
    municipality: Optional[str] = None
    year: Optional[str] = None
