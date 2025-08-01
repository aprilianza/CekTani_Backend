from pydantic import BaseModel
from typing import Dict, List

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str


class WeatherTemp(BaseModel):
    min: float
    max: float

class WeatherForecastDay(BaseModel):
    day: str
    date: str
    temp: WeatherTemp
    condition: str
    rainChance: float
    precipitation: float
    cloudCover: float
    windSpeed: float

class WeatherCurrent(BaseModel):
    temperature: float
    humidity: float
    condition: str
    rainChance: float
    windSpeed: float
    precipitation: float
    cloudCover: float

class WeatherAnalysisRequest(BaseModel):
    location: str
    current: WeatherCurrent
    forecast: List[WeatherForecastDay]

class WeatherAnalysisResponse(BaseModel):
    location: str
    analysis: str
