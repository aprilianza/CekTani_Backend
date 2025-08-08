import torch
from ultralytics import YOLO
import os
from PIL import Image
from io import BytesIO

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "yolo/classification.pt")

class_name_mapping = {
    "Apple___Apple_scab": "Apel - Kudis Apel",
    "Apple___Black_rot": "Apel - Busuk Hitam",
    "Apple___Cedar_apple_rust": "Apel - Karat Cedar",
    "Apple___healthy": "Apel - Sehat",
    "Blueberry___healthy": "Blueberry - Sehat",
    "Cherry_(including_sour)___Powdery_mildew": "Ceri - Embun Tepung",
    "Cherry_(including_sour)___healthy": "Ceri - Sehat",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Jagung - Bercak Daun Abu",
    "Corn_(maize)___Common_rust_": "Jagung - Karat Umum",
    "Corn_(maize)___Northern_Leaf_Blight": "Jagung - Hawar Daun Utara",
    "Corn_(maize)___healthy": "Jagung - Sehat",
    "Grape___Black_rot": "Anggur - Busuk Hitam",
    "Grape___Esca_(Black_Measles)": "Anggur - Esca (Campak Hitam)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Anggur - Hawar Daun",
    "Grape___healthy": "Anggur - Sehat",
    "Orange___Haunglongbing_(Citrus_greening)": "Jeruk - Citrus Greening",
    "Peach___Bacterial_spot": "Persik - Bercak Bakteri",
    "Peach___healthy": "Persik - Sehat",
    "Pepper,_bell___Bacterial_spot": "Paprika - Bercak Bakteri",
    "Pepper,_bell___healthy": "Paprika - Sehat",
    "Potato___Early_blight": "Kentang - Hawar Awal",
    "Potato___Late_blight": "Kentang - Hawar Akhir",
    "Potato___healthy": "Kentang - Sehat",
    "Raspberry___healthy": "Raspberry - Sehat",
    "Soybean___healthy": "Kedelai - Sehat",
    "Squash___Powdery_mildew": "Labu - Embun Tepung",
    "Strawberry___Leaf_scorch": "Stroberi - Daun Terbakar",
    "Strawberry___healthy": "Stroberi - Sehat",
    "Tomato___Bacterial_spot": "Tomat - Bercak Bakteri",
    "Tomato___Early_blight": "Tomat - Hawar Awal",
    "Tomato___Late_blight": "Tomat - Hawar Akhir",
    "Tomato___Leaf_Mold": "Tomat - Jamur Daun",
    "Tomato___Septoria_leaf_spot": "Tomat - Bercak Daun Septoria",
    "Tomato___Spider_mites Two-spotted_spider_mite": "Tomat - Tungau Laba-Laba",
    "Tomato___Target_Spot": "Tomat - Bercak Target",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "Tomat - Virus Keriting Daun Kuning",
    "Tomato___Tomato_mosaic_virus": "Tomat - Virus Mosaic",
    "Tomato___healthy": "Tomat - Sehat",
}

device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
model = YOLO(MODEL_PATH)



def classify_image_from_bytes(image_bytes: bytes):
    """
    Lakukan klasifikasi gambar langsung dari bytes tanpa perlu download/upload.
    
    Args:
        image_bytes: Bytes data dari gambar
        
    Returns:
        tuple: (translated_label, confidence)
    """
    try:
        # Konversi bytes ke PIL Image
        image = Image.open(BytesIO(image_bytes))
        
        # YOLO bisa menerima PIL Image langsung
        results = model.predict(source=image, device=device, verbose=False)
        r = results[0]

        class_index = int(r.probs.top1)
        confidence = float(r.probs.top1conf)
        class_name = r.names[class_index]
        translated_label = class_name_mapping.get(class_name, class_name)

        return translated_label, confidence
    
    except Exception as e:
        raise Exception(f"Error in image classification: {str(e)}")

