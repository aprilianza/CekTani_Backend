import google.generativeai as genai
from config import GEMINI_API_KEY
from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.schema import Document
from typing import List

# Konfigurasi API
genai.configure(api_key=GEMINI_API_KEY)

# Inisialisasi model Gemini Flash
model = genai.GenerativeModel("gemini-2.0-flash")

# Inisialisasi komponen RAG di level global
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = Chroma(persist_directory="chroma_store", embedding_function=embeddings)
retriever = vectorstore.as_retriever()

# Template prompt khusus botani
system_template = """
Kamu adalah pak tani seorang asisten botani yang membantu menjawab pertanyaan seputar:
- budidaya tanaman
- perawatan tanaman
- pengendalian hama
- pemupukan
- jenis tanaman

Kamu diberi potongan informasi dari berbagai dokumen. Jika potongan konteks mengandung informasi yang **relevan dengan pertanyaan**, gunakanlah konteks tersebut untuk menjawab dengan jelas dan akurat.

Jika **tidak ada informasi relevan** di konteks, kamu jawab dengan informasi yang kamu punya yang penting terkait tanaman.

Jika pertanyaannya **tidak berkaitan dengan tanaman atau botani**, balas dengan:
"Maaf, saya hanya menjawab pertanyaan seputar tanaman."

Berikut konteks yang diberikan:
{context}
"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("""Riwayat percakapan:
{chat_history}
Pengguna: {question}
Asisten:""")
]
prompt = ChatPromptTemplate.from_messages(messages)

# Inisialisasi LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.2
)

# Memory untuk menyimpan riwayat percakapan
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    output_key="answer"
)

# Chain untuk RAG
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
    combine_docs_chain_kwargs={"prompt": prompt},
    return_source_documents=True
)

def chat_with_bot(user_question: str) -> str:
    try:
        # Eksekusi chain
        result = qa_chain.invoke({
            "question": user_question,
            "chat_history": qa_chain.memory.chat_memory.messages
        })
        
        # Dapatkan jawaban
        bot_response = result["answer"]        
        
        return bot_response
    
    except Exception as e:
        print(f"Error di RAG chain: {str(e)}")

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
    response = model.generate_content(prompt)
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
        response = model.generate_content(prompt)
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