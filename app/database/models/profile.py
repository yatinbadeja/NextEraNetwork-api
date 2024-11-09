from pydantic import BaseModel, Field, constr, HttpUrl
from typing import Optional, List, Dict, Union
from uuid import uuid4
import datetime
from . import CommonData
from app.schema.enums import GenderType,CategoryType,StateType

class ProfileBase(BaseModel):
    firstname: str = ""
    middlename : str = ""
    lastname : str = ""
    gender : GenderType = GenderType.male
    abcID : str= ""
    category : CategoryType = CategoryType.gen
    profession : str =""
    position : str =""
    state : str
    about : Optional[str]
    passOut_Year : int = 2024
    skills: List[str] = []
    hobbies: List[str] =[]
    links: List[dict] = []
    languages: List[str] = []
    university : str = ""
    college: str = ""
    department : str = ""
    courses : str = ""
    branch : str = ""
    enrollmentNumber: str = ""
    enrollmentID : List[str] = []


class ProfileDB(ProfileBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    coverImage: Union[str,None] = None
    profileImage : Union[str,None] = None
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))

