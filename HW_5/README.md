# User Auth Project (SQLite)

Простий проєкт авторизації користувачів з використанням SQLite3.

## 📂 Структура проєкту
```plaintext
user_auth_project/
├── db/
│   ├── database.py
│   └── schema.sql
├── models/
│   └── user.py
├── main.py
├── tests/
│   ├── test_user_model.py
│   └── test_database.py
├── requirements.txt
└── README.md
```
## 🚀 Встановлення та запуск

### 1. Створення віртуального середовища
```commandline
python -m venv venv
venv\Scripts\activate  # Windows
```

### 2. Встановлення залежностей
```commandline
pip install -r requirements.txt
```

### 3. Запуск тестів
```commandline
pytest -q
```
### 4. Запуск програми
```commandline
python main.py
```