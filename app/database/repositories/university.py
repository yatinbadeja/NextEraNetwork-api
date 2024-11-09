from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.university import UniversityBase,UniversityDB
from app.database.repositories.sequence import sequence_repo

async def generate_university_id():
    sequence_id = await sequence_repo.increment_sequence_number("university_sequence")
    return f"University-{sequence_id:04d}"


class universityRepository(BaseMongoDbCrud[UniversityDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "university"
        )
    
    async def new(self, data: UniversityBase):
        user = await self.save(UniversityDB(**data.model_dump(),_id= await generate_university_id()))
        return user.id

university_repo = universityRepository()