# schemas/plant_schema.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class DiagnosisResponse(BaseModel):
    id: str
    result: str
    confidence: float
    notes: str
    photo_url: Optional[str] = None
    checked_at: datetime


class PlantCreate(BaseModel):
    name: str
    description: Optional[str] = None

class PlantResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    diagnosis: List[DiagnosisResponse] = []

