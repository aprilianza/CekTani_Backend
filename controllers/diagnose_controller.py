# routers/diagnosis_router.py

from datetime import datetime
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from bson import ObjectId
from models.user_model import User
from models.plant_model import Plant
from services.diagnosis_service import diagnose_only, process_diagnosis
from utils.security import get_current_user

router = APIRouter()

@router.post("/quick")
async def quick_diagnose(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    result = await diagnose_only(file, current_user.id)
    return result


@router.post("/{plant_id}")
async def diagnose_plant(
    plant_id: str,
    file: UploadFile = File(...),
    checked_at: datetime = Form(...), 
    current_user: User = Depends(get_current_user)
):
    plant = await Plant.get(ObjectId(plant_id))
    if plant is None or plant.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Plant not found or not yours")

    result = await process_diagnosis(plant, file, current_user.id, checked_at)
    return result

