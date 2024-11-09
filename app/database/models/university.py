from pydantic import BaseModel, Field
from typing import List
import datetime 
from uuid import uuid4
from app.schema.enums import UniversityType

class UniversityBase(BaseModel):
    universityName: str = ""
    universityImage : str = ""
    address : str = ""  

class UniversityDB(UniversityBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
