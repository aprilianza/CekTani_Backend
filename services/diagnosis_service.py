import os
from datetime import datetime
from fastapi import UploadFile, HTTPException
from models.diagnosis_model import Diagnosis
from models.plant_model import Plant
from services.yolo_service import classify_image_from_bytes
from services.gemini_service import explain_disease
from bson import ObjectId
import cloudinary
import cloudinary.uploader
from io import BytesIO

# Konfigurasi Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

async def upload_to_cloudinary(file_content: bytes, user_id: ObjectId) -> dict:
    """
    Upload gambar ke Cloudinary dengan folder sesuai user_id
    Return: Dictionary berisi URL dan public_id
    """
    try:
        # Upload ke Cloudinary
        upload_result = cloudinary.uploader.upload(
            BytesIO(file_content),
            folder=f"plant_diagnosis/{user_id}",
            resource_type="image"
        )
        
        return {
            "url": upload_result["secure_url"],
            "public_id": upload_result["public_id"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload image: {str(e)}")

async def process_diagnosis(plant: Plant, file: UploadFile, user_id: ObjectId, checked_at: datetime):
    try:
        # Baca file ke memory sekali saja
        file_content = await file.read()
        
        # Proses diagnosis langsung dari bytes (tidak perlu download dari Cloudinary)
        result, confidence = classify_image_from_bytes(file_content)
        explanation = explain_disease(result, confidence)
        
        # Upload gambar ke Cloudinary untuk penyimpanan
        cloudinary_result = await upload_to_cloudinary(file_content, user_id)

        diagnosis = Diagnosis(
            result=result,
            confidence=confidence,
            notes=explanation,
            photo_url=cloudinary_result["url"],
            photo_public_id=cloudinary_result["public_id"],
            checked_at=checked_at 
        )
        
        plant.diagnosis.append(diagnosis)
        await plant.save()

        return {
            "photo_url": cloudinary_result["url"],
            "result": result,
            "confidence": round(confidence, 4),
            "notes": explanation,
            "checked_at": checked_at.isoformat(),
            "message": "Diagnosis saved to database successfully."
        }
    except Exception as e:
        # Jika ada error, hapus gambar yang sudah diupload (jika ada)
        if 'cloudinary_result' in locals() and 'public_id' in cloudinary_result:
            try:
                cloudinary.uploader.destroy(cloudinary_result["public_id"])
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")

async def diagnose_only(file: UploadFile, user_id: ObjectId):
    """
    Diagnosis cepat tanpa upload ke Cloudinary
    """
    try:
        # Baca file ke memory
        file_content = await file.read()
        
        # Proses diagnosis langsung dari bytes
        result, confidence = classify_image_from_bytes(file_content)
        explanation = explain_disease(result, confidence)

        return {
            "result": result,
            "confidence": round(confidence, 4),
            "notes": explanation,
            "message": "Quick diagnosis successful. No image stored."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diagnosis failed: {str(e)}")
    
async def delete_diagnosis(plant_id: str, diagnosis_id: str, user_id: ObjectId) -> dict:
    plant = await Plant.get(ObjectId(plant_id))
    if not plant or plant.user_id != user_id:
        raise HTTPException(status_code=404, detail="Plant not found")
    
    # Find the diagnosis to delete
    diagnosis_to_delete = None
    for idx, diagnosis in enumerate(plant.diagnosis):
        if str(diagnosis.id) == diagnosis_id:
            diagnosis_to_delete = diagnosis
            break
    
    if not diagnosis_to_delete:
        raise HTTPException(status_code=404, detail="Diagnosis not found")
    
    # Delete image from Cloudinary
    if hasattr(diagnosis_to_delete, 'photo_public_id') and diagnosis_to_delete.photo_public_id:
        try:
            cloudinary.uploader.destroy(diagnosis_to_delete.photo_public_id)
        except Exception as e:
            print(f"Failed to delete image from Cloudinary {diagnosis_to_delete.photo_public_id}: {e}")
    
    # Remove diagnosis from plant
    plant.diagnosis.pop(idx)
    await plant.save()
    
    return {"detail": "Diagnosis deleted successfully"}