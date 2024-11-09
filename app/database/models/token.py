import datetime
from uuid import uuid4
from typing import List,Union
from pydantic import BaseModel, Field

from app.database.models import CommonData
from app.schema.enums import Roles


class RefreshTokenCreate(BaseModel):
    refresh_token: str
    user_id: str
    user_type: Roles
    username : str
    email : str
    profile_id : Union[str,None] = None


class RefreshTokenDB(RefreshTokenCreate):
    id: str = Field(default_factory=lambda: str(uuid4()), alias="_id")
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )


class RefreshTokenOut(RefreshTokenCreate, CommonData): ...
