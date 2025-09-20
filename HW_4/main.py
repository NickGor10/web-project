import pytest
from math_utils import add_numbers
from weather_utils import get_weather

def check_add_numbers():
    """Перевірка функції додавання та демонстрація результату."""
    print("=== Перевірка функції add_numbers ===")
    a, b = 5, 7
    result = add_numbers(a, b)
    print(f"{a} + {b} = {result}\n")

def run_tests():
    """Запускає тести та виводить лог."""
    print("=== Перевірка функціоналу проекту (тести) ===")
    result = pytest.main(["-q", "--tb=short"])
    if result == 0:
        print("Всі тести пройдено успішно!\n")
    else:
        print("Деякі тести не пройшли!\n")

def interactive_weather():
    """Інтерактивний режим запиту погоди."""
    print("=== Інтерактивний режим: запит погоди ===")
    print("Введіть 'exit', щоб вийти\n")

    while True:
        city = input("Введіть назву міста: ").strip()
        if city.lower() == "exit":
            print("Вихід з програми...")
            break
        if not city:
            print("Будь ласка, введіть назву міста.")
            continue

        try:
            weather_data = get_weather(city)
            temp = weather_data['main']['temp']
            desc = weather_data['weather'][0]['description']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            print(f"\nПогода в {city}:")
            print(f"  Температура: {temp}°C")
            print(f"  Опис: {desc}")
            print(f"  Вологість: {humidity}%")
            print(f"  Швидкість вітру: {wind_speed} м/с\n")
        except Exception as e:
            print(f"Не вдалося отримати погоду для '{city}': {e}\n")

def main():
    # 1. Перевірка функції додавання
    check_add_numbers()

    # 2. Перевірка функціоналу (тести)
    run_tests()

    # 3. Інтерактивний режим погоди
    interactive_weather()

if __name__ == "__main__":
    main()
