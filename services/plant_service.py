from typing import List
from fastapi import HTTPException
from models.plant_model import Plant
from schemas.plant_schema import PlantCreate, PlantResponse, DiagnosisResponse
from bson import ObjectId
import cloudinary
import cloudinary.uploader
import os

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

async def get_all_plants_by_user(user_id: str) -> List[PlantResponse]:
    plants = await Plant.find(Plant.user_id == user_id).to_list()
    return [map_plant_to_response(p) for p in plants]

async def get_plant_by_id(plant_id: str, user_id: str) -> PlantResponse:
    plant = await Plant.get(ObjectId(plant_id))
    if not plant or plant.user_id != user_id:
        raise HTTPException(status_code=404, detail="Plant not found")
    return map_plant_to_response(plant)

async def create_new_plant(data: PlantCreate, user_id: str) -> PlantResponse:
    plant = Plant(
        user_id=user_id,
        name=data.name,
        description=data.description
    )
    await plant.insert()
    return map_plant_to_response(plant)

async def delete_plant_by_id(plant_id: str, user_id: str) -> dict:
    plant = await Plant.get(ObjectId(plant_id))
    if not plant or plant.user_id != user_id:
        raise HTTPException(status_code=404, detail="Plant not found")

    # Hapus gambar dari Cloudinary
    for diagnosis in plant.diagnosis:
        if hasattr(diagnosis, 'photo_public_id') and diagnosis.photo_public_id:
            try:
                cloudinary.uploader.destroy(diagnosis.photo_public_id)
            except Exception as e:
                print(f"Failed to delete image from Cloudinary {diagnosis.photo_public_id}: {e}")

    await plant.delete()
    return {"detail": "Plant and associated diagnosis images deleted from Cloudinary"}

def map_diagnosis(diagnosis) -> DiagnosisResponse:
    return DiagnosisResponse(
        id=str(diagnosis.id),
        result=diagnosis.result,
        confidence=diagnosis.confidence,
        notes=diagnosis.notes,
        photo_url=diagnosis.photo_url,
        checked_at=diagnosis.checked_at
    )

def map_plant_to_response(plant) -> PlantResponse:
    diagnosis_list = [map_diagnosis(d) for d in plant.diagnosis]
    return PlantResponse(
        id=str(plant.id),
        name=plant.name,
        description=plant.description,
        diagnosis=diagnosis_list
    )