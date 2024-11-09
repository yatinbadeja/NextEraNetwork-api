from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.college import CollegeBase,CollegeDB
from app.database.repositories.sequence import sequence_repo

async def generate_college_id():
    sequence_id = await sequence_repo.increment_sequence_number("college_sequence")
    return f"COLLEGE-{sequence_id:04d}"


class collegeRepository(BaseMongoDbCrud[CollegeDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "college"
        )
    
    async def new(self, data: CollegeBase):
        user = await self.save(CollegeDB(**data.model_dump(),_id=await generate_college_id()))
        return user.id

college_repo = collegeRepository()