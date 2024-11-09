from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.achievement import AchievementBase,AchievementDB
from app.database.repositories.sequence import sequence_repo

async def generate_achievement_id():
    sequence_id = await sequence_repo.increment_sequence_number("achievement_sequence")
    return f"LEAVE-{sequence_id:04d}"

class achievementRepository(BaseMongoDbCrud[AchievementDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "achievements"
        )
    
    async def new(self, data: AchievementBase):
        user = await self.save(AchievementDB(**data.model_dump(),_id=await generate_achievement_id()))
        return user.id

achievement_repo = achievementRepository()