from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.experience import ExperienceBase,ExperienceDB
from app.database.repositories.sequence import sequence_repo

async def generate_experience_id():
    sequence_id = await sequence_repo.increment_sequence_number("experience_sequence")
    return f"EXPERIENCE-{sequence_id:04d}"


class experienceRepository(BaseMongoDbCrud[ExperienceDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "experience"
        )
        
    async def new(self, data: ExperienceBase):
        user = await self.save(ExperienceDB(**data.model_dump(),_id=await generate_experience_id()))
        return user.id

experience_repo = experienceRepository()