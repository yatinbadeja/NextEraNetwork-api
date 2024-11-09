from pydantic import BaseModel
from app.schema.enums import Roles,GenderType,CategoryType,StateType,JobModeType
from typing import Optional,List,Dict,Union
import datetime
class userCreate(BaseModel):
    username : str
    email: str
    accountType : Roles= Roles.Student

class experienceCreate(BaseModel):
    jobTitle : str
    experienceType : str
    companyName : str
    description : Union[str, None]
    jobMode : JobModeType = JobModeType.remote
    location: Union[str, None]
    start_date : str
    end_date : str
    continuing:bool = False

class EducationCreate(BaseModel):
    insitutionName : str
    degree: str
    field_of_study : str
    start_date : str
    end_date : str
    grade : Union[int, None]
    description : Union[str, None]
    
class CertificationCreate(BaseModel):
    profile_id : str
    certificationName : Optional[str] = None
    issuingOrganization : Optional[str] = None
    certificateURL : Optional[str] = None
    issue_date : Optional[str] = None
    expiry_date : Optional[str] = None
    description : Optional[str] = None

class AchievementCreate(BaseModel):
    title : str
    description : Union[str, None]
    date_achieved : Union[str, None]
    awardingOrganization : Union[str, None]
    
class ProjectCreate(BaseModel):
    projectName : Optional[str] = None
    description : Optional[str] = None
    technology: List[str] = []
    projectURL : Optional[str] = None
    start_date : Optional[str] =None
    end_date : Optional[str] = None
