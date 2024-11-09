from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.user import UserBase, UserDB
from app.database.repositories.sequence import sequence_repo

async def generate_user_id():
    sequence_id = await sequence_repo.increment_sequence_number("user_sequence")
    return f"LEAVE-{sequence_id:04d}"


class userRepository(BaseMongoDbCrud[UserDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "user"
        )
    
    async def new(self, data: UserBase):
        user = await self.save(UserDB(**data.model_dump(),_id=await generate_user_id())) 
        return user.id

user_repo = userRepository()