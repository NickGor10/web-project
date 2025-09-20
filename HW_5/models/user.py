import re
import sqlite3
from db.database import get_connection

class User:
    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def is_valid_email(self):
        """Перевірка email через regex"""
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(pattern, self.email) is not None

    def register(self):
        """Реєстрація користувача у БД"""
        if not self.is_valid_email():
            raise ValueError(f"Невалідний email: {self.email}")

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                (self.username, self.password, self.email)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            print(f"Помилка реєстрації: {e}")
            return False
        finally:
            conn.close()

    @classmethod
    def login(cls, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        return user is not None
