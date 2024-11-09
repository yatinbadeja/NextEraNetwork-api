from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from app.Config import ENV_PROJECT

# from app.database.models.sequence import
from .crud.base_mongo_crud import BaseMongoDbCrud
from ..models.sequence import Sequence


class SequenceRepository(BaseMongoDbCrud[Sequence]):
    def __init__(self):
        super().__init__(
            ENV_PROJECT.MONGO_DATABASE, "sequence", unique_attributes=["name"]
        )

    async def get_sequence_number(self, sequence_name: str) -> int:
        # Find the sequence document by name and return its current sequence number
        sequence_document = await self.collection.find_one({"name": sequence_name})
        return sequence_document["seq"] if sequence_document else 1

    async def increment_sequence_number(self, sequence_name: str) -> int:
        # Increment the sequence number for the given sequence name and return the updated value
        try:
            updated_document = await self.collection.find_one_and_update(
                {"name": sequence_name},
                {"$inc": {"seq": 1}},
                upsert=True,
                return_document=True,
            )
            print(updated_document["seq"])
            return updated_document["seq"]
        except DuplicateKeyError:
            # If there was a duplicate key error (which shouldn't happen due to upsert), handle it
            raise RuntimeError("Duplicate sequence name found.")


sequence_repo = SequenceRepository()