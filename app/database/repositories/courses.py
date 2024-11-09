from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.course import CourseBase,CourseDB
from app.database.repositories.sequence import sequence_repo

async def generate_course_id():
    sequence_id = await sequence_repo.increment_sequence_number("course_sequence")
    return f"COURSES-{sequence_id:04d}"

class courseRepository(BaseMongoDbCrud[CourseDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "courses"
        )
    
    async def new(self, data: CourseBase):
        user = await self.save(CourseDB(**data.model_dump(),_id=await generate_course_id()))
        return user.id

course_repo = courseRepository()