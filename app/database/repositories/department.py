from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.department import DepartmentBase,DepartmentDB
from app.database.repositories.sequence import sequence_repo

async def generate_department_id():
    sequence_id = await sequence_repo.increment_sequence_number("department_sequence")
    return f"DEPT-{sequence_id:04d}"


class departmentRepository(BaseMongoDbCrud[DepartmentDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "department"
        )
    
    async def new(self, data: DepartmentBase):
        user = await self.save(DepartmentDB(**data.model_dump(),_id= await generate_department_id()))
        return user.id
    
    
department_repo = departmentRepository()