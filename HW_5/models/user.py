from db.database import get_connection
from utils.validators import validate_email
from mysql.connector import IntegrityError

class User:
    def __init__(self, username, password, email):
        if not validate_email(email):
            raise ValueError("❌ Некоректний email")
        self.username = username
        self.password = password
        self.email = email

    def register(self):
        """Реєстрація користувача в MySQL."""
        self.username = self.username.strip().lower()
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (self.username, self.password, self.email)
            )
            conn.commit()
            return True
        except IntegrityError:
            return False
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def login(username, password):
        conn = get_connection()
        cursor = conn.cursor()
        username_clean = username.strip().lower()
        cursor.execute(
            "SELECT id FROM users WHERE LOWER(username)=%s AND password=%s",
            (username_clean, password)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return bool(result)
