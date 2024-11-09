from pydantic import BaseModel, Field, HttpUrl
from typing import Union, List,Optional
from uuid import uuid4
import datetime

class ProjectBase(BaseModel):
    profile_id : str
    projectName : Optional[str] = None
    description : Optional[str] = None
    technology: List[str] = []
    projectURL : Optional[str] = None
    start_date : Optional[datetime.datetime] =None
    end_date : Optional[datetime.datetime] = None

class ProjectDB(ProjectBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))