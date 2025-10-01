import requests

# Параметри запиту
city = "Kyiv"
api_key = "079e9a07c1b5b790d6465e50434c7d46"
url = "https://api.openweathermap.org/data/2.5/weather"

# Робимо GET-запит
response = requests.get(url, params={
    "q": city,
    "appid": api_key,
    "units": "metric"
})

# Перевірка статусу відповіді
if response.status_code == 200:
    data = response.json()
    print(f"Погода в {data['name']}: {data['main']['temp']}°C")

    # Перевірка наявності основних полів
    assert "weather" in data, "Поле weather відсутнє"
    assert "main" in data, "Поле main відсутнє"
    assert data["name"] == city, f"Назва міста не збігається: {data['name']}"

    print("Запит успішний і дані вірні!")
else:
    print(f"Помилка запиту: {response.status_code} \n {response.text}")
