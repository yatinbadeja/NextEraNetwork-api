from typing import Literal, Optional, Union

from pydantic import BaseModel


class BaseToken(BaseModel):
    access_token: str
    refresh_token: str
    scope: str


class TokenData(BaseModel):
    user_id: str
    username : str
    email : str
    profile_id : Union[str, None] = None
    user_type: Literal["University", "College", "Student"] = "Student"
    scope: Literal["login", "forgot_password"] = "login"


class RefreshTokenPost(BaseModel):
    refresh_token: str


class OnlyRefreshToken(BaseModel):
    refresh_token: str
