from pydantic import BaseModel, Field
from typing import List
import datetime
from uuid import uuid4
from app.schema.enums import CourseType

class CourseBase(BaseModel):
    university_id : str = ""
    college_id :str = ""
    department_id : str = ""
    courseName: CourseType = CourseType.Btech

class CourseDB(CourseBase):
    id : str = Field(default_factory=lambda : str(uuid4()), alias='_id')
    created_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
    updated_at: datetime.datetime = Field(default_factory=lambda : datetime.datetime.now(datetime.timezone.utc))
