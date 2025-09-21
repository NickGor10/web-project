import sqlite3

# Глобальна змінна, яку можуть підмінити тести через monkeypatch
DB_NAME = "products.db"


def get_connection():
    """Повертає підключення до SQLite, використовуючи глобальну змінну DB_NAME."""
    return sqlite3.connect(DB_NAME)


def init_db():
    """Ініціалізує таблицю products (створює якщо ще не існує)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            link TEXT,
            rating TEXT
        )
    """)
    conn.commit()
    conn.close()
