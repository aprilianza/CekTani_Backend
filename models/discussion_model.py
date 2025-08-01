# models/discussion_model.py
from beanie import Document
from pydantic import Field, BaseModel
from typing import List
from datetime import datetime
from bson import ObjectId

class Reply(BaseModel):
    user_id: ObjectId
    content: str
    created_at: datetime 

    class Config:
        arbitrary_types_allowed = True

class Discussion(Document):
    user_id: ObjectId
    title: str
    content: str
    replies: List[Reply] = Field(default_factory=list)
    created_at: datetime 

    class Settings:
        name = "discussions"

    class Config:
        arbitrary_types_allowed = True
