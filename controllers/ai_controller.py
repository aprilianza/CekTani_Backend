from fastapi import APIRouter, HTTPException, Depends
from models.user_model import User
from services.gemini_service import chat_with_bot, analyze_weather_for_plants
from schemas.ai_schema import ChatRequest, ChatResponse, WeatherAnalysisRequest, WeatherAnalysisResponse
from utils.security import get_current_user

router = APIRouter()

@router.post("/chatbot", response_model=ChatResponse)
async def chat(request: ChatRequest, current_user: User = Depends(get_current_user)):
    try:
        response = chat_with_bot(request.question)
        return {"answer": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Terjadi kesalahan: {str(e)}")

@router.post("/weather/analyze", response_model=WeatherAnalysisResponse)
async def analyze_weather(
    request: WeatherAnalysisRequest, 
    current_user: User = Depends(get_current_user)
):
    """
    Analyze weather conditions and provide plant care recommendations.
    """
    try:
        # Validate weather data
        if not request.location or not request.current or not request.forecast:
            raise HTTPException(
                status_code=400,
                detail="Lengkapi data lokasi, kondisi saat ini, dan prakiraan cuaca"
            )

        # Convert Pydantic models to dict
        current_dict = request.current.dict()
        forecast_dict = [day.dict() for day in request.forecast]

        # Prepare weather data dictionary
        weather_data = {
            "location": request.location,
            "current": current_dict,
            "forecast": forecast_dict
        }

        # Get analysis from Gemini
        analysis = analyze_weather_for_plants(weather_data)
        
        return {
            "location": request.location,
            "analysis": analysis,
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Gagal menganalisis cuaca: {str(e)}"
        )