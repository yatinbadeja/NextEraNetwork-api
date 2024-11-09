from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.branch import BranchBase,BranchDB
from app.database.repositories.sequence import sequence_repo

async def generate_branch_id():
    sequence_id = await sequence_repo.increment_sequence_number("branch_sequence")
    return f"BRANCH-{sequence_id:04d}"

class branchRepository(BaseMongoDbCrud[BranchDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "branch"
        )
    
    async def new(self, data: BranchBase):
        user = await self.save(BranchDB(**data.model_dump(),_id=await generate_branch_id()))
        return user.id

branch_repo = branchRepository()