# schemas/discussion_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class DiscussionCreate(BaseModel):
    title: str
    content: str
    created_at: Optional[datetime] = None

class ReplyCreate(BaseModel):
    content: str
    created_at: Optional[datetime] = None  

class ReplyResponse(BaseModel):
    user_id: str
    username: Optional[str] = None 
    content: str
    created_at: datetime

class DiscussionResponse(BaseModel):
    id: str
    user_id: str
    username: Optional[str] = None
    title: str
    content: str
    replies: List[ReplyResponse]
    created_at: datetime

