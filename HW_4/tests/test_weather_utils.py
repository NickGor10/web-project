import pytest
from weather_utils import get_weather
import os

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@pytest.mark.skipif(not API_KEY, reason="API key not set in .env")
def test_get_weather_structure():
    """Перевірка базової структури JSON"""
    city = "Kyiv"
    data = get_weather(city)
    assert "main" in data
    assert "temp" in data["main"]
    assert "humidity" in data["main"]
    assert "weather" in data
    assert isinstance(data["weather"], list)
    assert "description" in data["weather"][0]
    assert "name" in data and data["name"].lower() == city.lower()

@pytest.mark.skipif(not API_KEY, reason="API key not set in .env")
def test_temperature_type():
    """Перевірка типу температури"""
    city = "London"
    data = get_weather(city)
    temp = data["main"]["temp"]
    assert isinstance(temp, (int, float))

@pytest.mark.skipif(not API_KEY, reason="API key not set in .env")
def test_weather_description_non_empty():
    """Перевірка на непорожній опис погоди"""
    city = "New York"
    data = get_weather(city)
    desc = data["weather"][0]["description"]
    assert isinstance(desc, str) and len(desc) > 0

@pytest.mark.skipif(not API_KEY, reason="API key not set in .env")
def test_humidity_and_wind():
    """Перевірка вологість і швидкості вітру"""
    city = "Berlin"
    data = get_weather(city)
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    assert isinstance(humidity, (int, float)) and 0 <= humidity <= 100
    assert isinstance(wind_speed, (int, float)) and wind_speed >= 0

@pytest.mark.skipif(not API_KEY, reason="API key not set in .env")
def test_api_status_code():
    """Перевірка коду статусу HTTP через requests"""
    import requests
    city = "Tokyo"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    assert response.status_code == 200
