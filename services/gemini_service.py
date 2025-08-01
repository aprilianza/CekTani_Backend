import google.generativeai as genai
from config import GEMINI_API_KEY

# Konfigurasi API
genai.configure(api_key=GEMINI_API_KEY)

# Inisialisasi model Gemini Flash
model = genai.GenerativeModel("gemini-2.0-flash")

# Instruction khusus untuk chatbot tanaman
BOTANICAL_INSTRUCTION = (
    "Kamu adalah asisten ahli botani. "
    "Jawablah semua pertanyaan hanya tentang tanaman: budidaya, perawatan, hama, pemupukan, jenis tanaman, dan lainnya. "
    "Jika pertanyaan tidak terkait tanaman, balas dengan: 'Maaf, saya hanya menjawab tentang tanaman.'"
)

def explain_disease(disease_name: str, confidence: float) -> str:
    """Berikan penjelasan tentang penyakit tanaman"""
    confidence_percent = confidence * 100
    prompt = (
        f"Saya mendeteksi penyakit tanaman bernama: {disease_name}. "
        "Jelaskan penyakit ini, gejalanya, dan bagaimana cara mengatasinya. "
        "Berikan informasi seakurat mungkin dan seringkas mungkin untuk petani pemula. "
        f"jawab dengan awalan saya 'saya yakin {confidence_percent:.2f}% bahwa penyakit ini adalah {disease_name}'"
        "jika confidence kurang dari 0.5, katakan 'Saya tidak yakin penyakit ini, silakan konsultasikan dengan ahli tanaman.'"
    )
    chat = model.start_chat()
    response = chat.send_message(prompt)
    return response.text

def chat_with_bot(user_question: str) -> str:
    # Gabungkan instruction + input pengguna
    full_prompt = f"{BOTANICAL_INSTRUCTION}\n\n{user_question}"
    chat = model.start_chat()
    response = chat.send_message(full_prompt)
    return response.text

def analyze_weather_for_plants(weather_data: dict) -> str:
    # Prepare the prompt for Gemini
    prompt = f"""
    Anda adalah ahli agronomi dan botani. Berikan analisis cuaca untuk perawatan tanaman berdasarkan data berikut:
    
    Lokasi: {weather_data.get('location', 'Unknown')}
    
    Kondisi Saat Ini:
    - Suhu: {weather_data['current']['temperature']}°C
    - Kelembaban: {weather_data['current']['humidity']}%
    - Kondisi: {weather_data['current']['condition']}
    - Curah Hujan: {weather_data['current']['precipitation']}mm
    - Kecepatan Angin: {weather_data['current']['windSpeed']} km/jam
    
    Prakiraan 3 Hari:
    {format_forecast(weather_data['forecast'])}
    
    Berikan:
    1. Analisis singkat kondisi cuaca saat ini untuk tanaman
    2. Rekomendasi perawatan tanaman berdasarkan cuaca saat ini
    3. Persiapan yang diperlukan untuk menghadapi prakiraan cuaca mendatang
    4. Peringatan khusus jika ada kondisi ekstrim yang berbahaya untuk tanaman
    5. Jenis tanaman yang cocok untuk kondisi cuaca saat ini
    
    Sertakan tips praktis untuk petani/pemilik tanaman. Gunakan bahasa yang sederhana dan mudah dimengerti.
    """
    
    try:
        chat = model.start_chat()
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error generating weather analysis: {str(e)}"

def format_forecast(forecast_data: list) -> str:
    """Helper function to format forecast data for the prompt"""
    forecast_text = ""
    for day in forecast_data:
        forecast_text += (
            f"\n- {day['day']} ({day['date']}): "
            f"Suhu {day['temp']['min']}°C-{day['temp']['max']}°C, "
            f"{day['condition']}, "
            f"Hujan: {day['precipitation']}mm, "
            f"Angin: {day['windSpeed']} km/jam\n"
        )
    return forecast_text