import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE
MONGO_URI = os.getenv("MONGO_URI")

# JWT
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"

# GEMINI API 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
