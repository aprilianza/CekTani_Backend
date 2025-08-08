---

# **CekTani – Backend API Documentation**

Backend ini merupakan bagian dari platform **CekTani**, sebuah website pertanian digital berbasis **FastAPI** yang membantu petani mendeteksi penyakit tanaman, menganalisis cuaca, berkonsultasi dengan asisten virtual, dan berdiskusi melalui forum komunitas.

Backend menangani logika bisnis inti, autentikasi, pengelolaan data tanaman, integrasi model AI, dan komunikasi dengan database.

---

## **1. Arsitektur Backend**

- **Framework**: FastAPI – API cepat dan modern berbasis Python.
- **Database**:
    - **MongoDB** → penyimpanan data pengguna, tanaman, diagnosis, dan forum diskusi.
    - **ChromaDB** → penyimpanan vektor untuk mendukung pencarian semantik di chatbot *Pak Tani* (RAG).
    - **Cloudinary** → penyimpanan gambar berbasis cloud.
- **Model AI**:
    - **YOLOv11n** untuk deteksi penyakit tanaman berbasis gambar daun.
    - **Google Gemini** (LLM) untuk asisten virtual berbasis teks.
- **Autentikasi**: JWT (JSON Web Token).
- **Deploy**: kompatibel untuk server lokal maupun cloud.

---

## **2. Base URL**

```

http://localhost:8000

```

Untuk server produksi, ganti dengan domain deployment.

---

## **3. Authentication**

Semua endpoint kecuali `register` dan `login` membutuhkan **Bearer Token** JWT.

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **POST** | `/auth/register` | Registrasi akun pengguna baru. |
| **POST** | `/auth/login` | Login dan mendapatkan JWT token. |
| **GET** | `/auth/me` | Mendapatkan profil pengguna yang sedang login. |

**Contoh Request Login:**

```json

{
  "email": "arnold@gmail.com",
  "password": "user123"
}

```

---

## **4. Plants Resource**

Mengelola data tanaman.

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **GET** | `/plants/` | Mengambil semua data tanaman. |
| **POST** | `/plants/` | Menambahkan data tanaman baru. |
| **GET** | `/plants/{plant_id}` | Mendapatkan detail tanaman berdasarkan ID. |
| **PUT** | `/plants/{plant_id}` | Memperbarui data tanaman. |
| **DELETE** | `/plants/{plant_id}` | Menghapus data tanaman. |

**Contoh Request Create Plant:**

```json

{
  "name": "kentang goreng",
  "description": "Tanaman kentang milik saya di pekarangan rumah"
}

```

---

## **5. Diagnose Resource**

Fitur diagnosis penyakit tanaman berbasis AI.

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **POST** | `/diagnose/quick` | Diagnosis cepat tanpa ID tanaman. |
| **POST** | `/diagnose/{plant_id}` | Diagnosis penyakit pada tanaman tertentu. |
| **DELETE** | `/diagnose/{plant_id}/{diagnosis_id}` | Menghapus hasil diagnosis tertentu. |

**Contoh Request Quick Diagnose:**

```json
{
  "file": "base64_image_data_here"
  "checked_at": "base64_image_data_here"
}

```

---

## **6. AI Resource**

Integrasi AI untuk chatbot dan analisis cuaca.

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **POST** | `/ai/chatbot` | Bertanya ke asisten virtual *Pak Tani*. |
| **POST** | `/ai/weather/analyze` | Analisis cuaca untuk rekomendasi pertanian. |

**Contoh Request Chatbot:**

```json

{
  "question": "bagaimana cara mengatasinya?"
}

```

---

## **7. Discussions Resource**

Forum komunitas untuk berdiskusi antar petani.

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| **GET** | `/discussions/` | Menampilkan daftar diskusi. |
| **POST** | `/discussions/` | Membuat diskusi baru. |
| **POST** | `/discussions/{discussion_id}/reply` | Membalas diskusi tertentu. |
| **PUT** | `/discussions/{discussion_id}` | Mengedit diskusi. |
| **DELETE** | `/discussions/{discussion_id}` | Menghapus diskusi. |

**Contoh Request Create Discussion:**

```json
{
  "title": "Apa penyebab daun menguning?",
  "content": "Saya melihat daun tanaman cabai saya menguning.",
  "created_at": "2025-07-31T21:05:00+07:00"
}

```

---

## **8. Instalasi dan Menjalankan Backend**

```bash
bash
CopyEdit
# Clone repository
git clone https://github.com/username/cek-tani-backend.git
cd cek-tani-backend

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan server
uvicorn main:app --reload

```

---

## **9. Environment Variables**

Buat file `.env`:

```
MONGO_URI=
JWT_SECRET_KEY=
GEMINI_API_KEY=
CLOUDINARY_CLOUD_NAME = 
CLOUDINARY_API_KEY = 
CLOUDINARY_API_SECRET = 

```
