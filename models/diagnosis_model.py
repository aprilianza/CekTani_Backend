from pydantic import BaseModel, Field
from datetime import datetime
from beanie import PydanticObjectId
from typing import Optional

class Diagnosis(BaseModel):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    result: str
    confidence: float
    notes: str = ""
    photo_url: str
    checked_at: datetime
    photo_public_id: Optional[str] = None
