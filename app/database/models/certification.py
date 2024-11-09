from pydantic import BaseModel, Field, HttpUrl
from typing import Union, List,Optional
from uuid import uuid4
import datetime
from app.schema.enums import JobModeType

class CertificationBase(BaseModel):
    profile_id : str
    certificationName : Optional[str] = None
    issuingOrganization : Optional[str] = None
    certificateURL : Optional[str] = None
    issue_date : Optional[datetime.datetime] = None
    expiry_date : Union[datetime.datetime, None] = None
    description : Union[str, None] = None

class CertificationDB(CertificationBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
