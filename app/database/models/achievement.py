from pydantic import BaseModel, Field, HttpUrl
from typing import Union, List
from uuid import uuid4
import datetime
from app.schema.enums import JobModeType

class AchievementBase(BaseModel):
    profile_id : str
    title : str
    description : Union[str, None]
    date_achieved : Union[datetime.datetime, None]
    awardingOrganization : Union[str, None]

class AchievementDB(AchievementBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))