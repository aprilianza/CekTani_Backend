from fastapi import APIRouter, Depends
from typing import List
from services.plant_service import (
    get_all_plants_by_user,
    get_plant_by_id,
    create_new_plant,
    delete_plant_by_id
)
from utils.security import get_current_user
from models.user_model import User
from schemas.plant_schema import PlantCreate, PlantResponse

router = APIRouter()


@router.get("/", response_model=List[PlantResponse])
async def read_plants(current_user: User = Depends(get_current_user)):
    return await get_all_plants_by_user(current_user.id)


@router.get("/{plant_id}", response_model=PlantResponse)
async def read_plant(plant_id: str, current_user: User = Depends(get_current_user)):
    return await get_plant_by_id(plant_id, current_user.id)


@router.post("/", response_model=PlantResponse)
async def create_plant(data: PlantCreate, current_user: User = Depends(get_current_user)):
    return await create_new_plant(data, current_user.id)


@router.delete("/{plant_id}")
async def delete_plant(plant_id: str, current_user: User = Depends(get_current_user)):
    return await delete_plant_by_id(plant_id, current_user.id)