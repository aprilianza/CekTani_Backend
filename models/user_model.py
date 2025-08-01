from beanie import Document
from pydantic import Field
from datetime import datetime

class User(Document):
    email: str = Field(..., unique=True)
    username: str
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"
    class Config:
        arbitrary_types_allowed = True 
