import os
import shutil
from datetime import datetime
from fastapi import UploadFile
from models.diagnosis_model import Diagnosis
from models.plant_model import Plant
from services.yolo_service import classify_image
from services.gemini_service import explain_disease
from bson import ObjectId

BASE_DIR = "./images"

def save_image(file: UploadFile, user_id: ObjectId) -> tuple[str, str]:
    """
    Simpan gambar ke folder sesuai user_id.
    Return: file_path dan filename
    """
    user_folder = os.path.join(BASE_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(user_folder, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path, filename

async def process_diagnosis(plant: Plant, file: UploadFile, user_id: ObjectId, checked_at: datetime):
    file_path, filename = save_image(file, user_id)
    result, confidence = classify_image(file_path)
    explanation = explain_disease(result, confidence)

    diagnosis = Diagnosis(
        result=result,
        confidence=confidence,
        notes=explanation,
        photo_url=file_path,
        checked_at=checked_at 
    )
    plant.diagnosis.append(diagnosis)
    await plant.save()

    return {
        "photo_url": file_path,
        "result": result,
        "confidence": round(confidence, 4),
        "notes": explanation,
        "checked_at": checked_at.isoformat(),
        "message": "Diagnosis saved to database successfully."
    }

async def diagnose_only(file: UploadFile, user_id: ObjectId):
    """
    Diagnosis cepat tanpa menyimpan ke database (gambar akan dihapus setelah diagnosis)
    """
    file_path, filename = save_image(file, user_id)

    try:
        result, confidence = classify_image(file_path)
        explanation = explain_disease(result, confidence)

        return {
            "photo_url": filename,
            "result": result,
            "confidence": round(confidence, 4),
            "notes": explanation,
            "message": "Quick diagnosis successful. Image not saved and has been deleted."
        }

    finally:
        # Hapus file setelah proses selesai (berhasil maupun gagal)
        if os.path.exists(file_path):
            os.remove(file_path)

