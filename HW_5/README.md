# User Auth Project (MySQL)

## 📂 Структура проєкту
```plaintext
user_auth_project/
├── db/
│   └── database.py        # Підключення до MySQL + ініціалізація таблиці
├── models/
│   └── user.py            # Клас User (реєстрація + логін з MySQL)
├── utils/
│   └── validators.py      # Валідація email
├── tests/
│   ├── test_database.py   # Тести створення таблиці в MySQL
│   └── test_user_model.py # Тести класу User
├── main.py                # Інтерактивний CLI
├── requirements.txt
├── .env                   # Конфіг для MySQL
└── README.md
```
## 🚀 Встановлення та запуск
### 1. Клонування репозиторію
```commandline
git clone https://github.com/yourname/user_auth_project.git
cd вказати шлях до папки проекту
```

### 2. Створення віртуального середовища
```commandline
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Встановлення залежностей
```commandline
pip install -r requirements.txt
```
### 4. Налаштування .env
Створи файл .env в корені проекту та додати:
```commandline
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=user_auth_db
```
### 5. Ініціалізація БД
```commandline
python main.py  # Таблиця створиться автоматично
```
### 6. Запуск тестів
```commandline
pytest -q
```