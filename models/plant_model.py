from beanie import Document
from pydantic import Field
from typing import List
from datetime import datetime
from bson import ObjectId
from models.diagnosis_model import Diagnosis

class Plant(Document):
    user_id: ObjectId
    name: str
    description: str
    diagnosis: List[Diagnosis] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "plants"

    class Config:
        arbitrary_types_allowed = True
