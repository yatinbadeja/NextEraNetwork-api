from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.project import ProjectBase,ProjectDB
from app.database.repositories.sequence import sequence_repo

async def generate_project_id():
    sequence_id = await sequence_repo.increment_sequence_number("project_sequence")
    return f"PROJECT-{sequence_id:04d}"

class projectRepository(BaseMongoDbCrud[ProjectDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "project"
        )

    async def new(self, data: ProjectBase):
        user = await self.save(ProjectDB(**data.model_dump(),_id=await generate_project_id()))
        return user.id

project_repo = projectRepository()