from pydantic import BaseModel


class NameID(BaseModel):
    name: str
    id: int