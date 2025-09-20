import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    # "host": os.getenv("DB_HOST", "localhost"),
    # "port": int(os.getenv("DB_PORT", 3306)),
    # "user": os.getenv("DB_USER", "root"),
    # "password": os.getenv("DB_PASSWORD", ""),
    # "database": os.getenv("DB_NAME", "user_auth_db"),
    "host": "localhost",
    "user": "myuser",
    "password": "mypassword",
    "database": "users_db"
}

def get_connection():
    """Повертає підключення до MySQL."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"❌ Помилка підключення до MySQL: {e}")
        raise

def init_db():
    """Ініціалізація таблиці users з UNIQUE constraints"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            )
        """)
    conn.commit()
    cursor.close()
    conn.close()

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Таблиця користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    )
    """)

    # Нова таблиця для зберігання логінів на сайтах
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS site_credentials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        site_name VARCHAR(100) NOT NULL,
        login VARCHAR(100) NOT NULL,
        password VARCHAR(255) NOT NULL,
        login_type ENUM('google', 'apple', 'facebook', 'other') DEFAULT 'other',
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()