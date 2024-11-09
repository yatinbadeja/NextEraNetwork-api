from pydantic import BaseModel, Field
from typing import Union
from uuid import uuid4
import datetime

class EducationBase(BaseModel):
    profile_id : str 
    insitutionName : str
    degree: str
    field_of_study : str
    start_date : datetime.datetime
    end_date : datetime.datetime
    grade : Union[int, None]
    description : Union[str, None]

class EducationDB(EducationBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
