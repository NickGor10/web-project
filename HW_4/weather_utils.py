import requests
from dotenv import load_dotenv
import os

load_dotenv()


def get_weather(city: str) -> dict:
    """
    Fetch weather data for a given city from OpenWeatherMap API.

    Args:
        city (str): Name of the city

    Returns:
        dict: Parsed JSON response from the API
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("API ключ не заданий. Додайте його у .env")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
