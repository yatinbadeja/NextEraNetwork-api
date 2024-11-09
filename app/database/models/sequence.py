from pydantic import BaseModel
from uuid import uuid4
from pydantic import Field


class Sequence(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    name: str  # Unique identifier for the sequence
    seq: int  # Current sequence number