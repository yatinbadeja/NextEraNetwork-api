from pydantic import BaseModel, Field, HttpUrl
from typing import Union, List
from uuid import uuid4
import datetime
from app.schema.enums import JobModeType

class ExperienceBase(BaseModel):
    profile_id : str
    jobTitle : str
    experienceType : str
    companyName : str
    description : Union[str, None]
    jobMode : JobModeType = JobModeType.remote
    location: Union[str, None]
    start_date : Union[datetime.datetime, str] = ""
    end_date : Union[datetime.datetime, str] = ""
    continuing: bool= False


class ExperienceDB(ExperienceBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))