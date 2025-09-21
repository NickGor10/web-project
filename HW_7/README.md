# 📦 Rozetka Apple Phones Scraper

Цей проєкт виконує **веб-скрапінг** сторінок Rozetka для збору інформації про мобільні телефони **Apple**  
і зберігає ці дані у базу **SQLite**.  

Проєкт побудований з використанням **Python, BeautifulSoup4, SQLite, Pytest**  

---

## 🚀 Функціонал

✅ Скрипт дозволяє:  
- Ввести **кількість сторінок**, які хочете спарсити  
- Вибрати, які **поля даних** збирати:
  - `name` — назва товару  
  - `price` — ціна  
  - `link` — посилання на сторінку товару  
  - `rating` — рейтинг товару (якщо є на сторінці)  
- Автоматично **зберігати результати** у локальну SQLite базу `products.db`
- Переглядати збережені товари у консольному режимі після завершення скрапінгу  

---

## 🏗 Структура проєкту

```commandline
├── db/
│ ├── database.py # Ініціалізація SQLite, створення таблиць
│ └── models.py # Клас Product (ORM-like)
├── scraper/
│ ├── rozetka_scraper.py # Клас RozetkaScraper, логіка fetch + parse
│ └── utils.py # Допоміжні утиліти
├── tests/
│ ├── test_database.py # Тести для SQLite
│ └── test_scraper.py # Тести для парсера з mock-HTML
├── main.py # CLI-інтерфейс для запуску
├── requirements.txt
└── README.md
```
---

## 🛠 Встановлення

### #️⃣ Клонуйте репозиторій у нову гілку  
```bash
git clone ...
```
### 2️⃣ Створіть віртуальне оточення
```commandline
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

```
### 3️⃣ Встановіть залежності
```commandline
pip install -r requirements.txt
```

### ▶️ Запуск

```commandline
python main.py
```

### 🧪 Тести
```commandline
pytest -q
```