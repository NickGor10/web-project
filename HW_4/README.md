# Weather & Math Utils Project

## Опис
Цей проект демонструє дві функціональності:

1. **Функція додавання чисел** (`add_numbers`)  
   - Додає два числа і повертає суму.
2. **Функція отримання погоди з OpenWeatherMap** (`get_weather`)  
   - Робить HTTP-запит до API і повертає дані про погоду у форматі JSON.

## Структура проекту

weather_math_project/
├── math_utils.py # Функція додавання
├── weather_utils.py # Запит погоди через API
├── main.py # Інтерактивний запуск програми
├── tests/ # Тести проекту
│ ├── test_add_numbers.py
│ └── test_weather_utils.py
├── requirements.txt # Залежності проекту
└── README.md # Документація проекту

## Встановлення та запуск

### 1. Створення віртуального середовища
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2 Встановлення залежностей
```bash
pip install -r requirements.txt
```

### 3. Перевірка функцій
```bash
pytest -q
```

### 4. Запуск прикладів у main.py
```bash
python main.py
```

⚠️ Для функції get_weather потрібно вказати свій API ключ OpenWeatherMap у файлі .env  в корені проекту