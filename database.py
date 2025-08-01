from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user_model import User
from models.plant_model import Plant
from models.discussion_model import Discussion
from config import MONGO_URI
async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.tanishield_db
    await init_beanie(database=db, document_models=[User, Plant, Discussion])
