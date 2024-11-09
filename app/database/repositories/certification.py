from app.Config import ENV_PROJECT
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.certification import CertificationBase,CertificationDB
from app.database.repositories.sequence import sequence_repo


async def generate_certification_id():
    sequence_id = await sequence_repo.increment_sequence_number("certification_sequence")
    return f"CERTIFICATION-{sequence_id:04d}"


class certificationRepository(BaseMongoDbCrud[CertificationDB]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, 
            "certification"
        )
    
    async def new(self, data: CertificationBase):
        user = await self.save(CertificationDB(**data.model_dump(),_id=await generate_certification_id()))
        return user.id

certification_repo = certificationRepository()