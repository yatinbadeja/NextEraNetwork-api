from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.education import EducationBase,EducationDB
from app.database.repositories.sequence import sequence_repo

async def generate_education_id():
    sequence_id = await sequence_repo.increment_sequence_number("education_sequence")
    return f"LEAVE-{sequence_id:04d}"

class educationRepository(BaseMongoDbCrud[EducationDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "education"
        )
    
    async def new(self, data: EducationBase):
        user = await self.save(EducationDB(**data.model_dump))
        return user.id
    async def new(self, data: EducationBase):
        user = await self.save(EducationDB(**data.model_dump(),_id=await generate_education_id()))
        return user.id

education_repo = educationRepository()