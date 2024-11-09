from pydantic import BaseModel, Field, EmailStr, validator
from typing import Union, Optional
from uuid import  uuid4
import datetime
from enum import Enum
from bson import ObjectId
from app.schema.enums import Roles
from app.utils.hashing import hash_password

class UserBase(BaseModel):
    username : str
    email: str
    password : str
    accountType : Roles = Roles.Student
    profileID : Optional[str] = None
    

class UserDB(UserBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    
    
    @validator("password", pre=True, always=True)
    def convert_password_to_hash(cls, v: str) -> str:
        if v != "":
            v = hash_password(v)
        return v