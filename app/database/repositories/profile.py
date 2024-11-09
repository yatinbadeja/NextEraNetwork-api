from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.profile import ProfileBase,ProfileDB
from app.database.repositories.sequence import sequence_repo

async def generate_profile_id():
    sequence_id = await sequence_repo.increment_sequence_number("profile_sequence")
    return f"PROFILE-{sequence_id:04d}"


class profileRepository(BaseMongoDbCrud[ProfileDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "profile"
        )

    async def new(self, data: ProfileBase):
        user = await self.save(ProfileDB(**data.model_dump(),_id=await generate_profile_id()),)
        return user.id


profile_repo = profileRepository()