from db.database import get_connection

class SiteCredential:
    def __init__(self, user_id, site_name, login=None, password=None, login_type="other"):
        self.user_id = user_id
        self.site_name = site_name
        self.login = login
        self.password = password
        self.login_type = login_type

    def add(self):
        conn = get_connection()
        cursor = conn.cursor()
        # Перевіримо чи вже є такий site + user_id + login_type
        cursor.execute(
            "SELECT id FROM site_credentials WHERE user_id=%s AND site_name=%s AND login_type=%s",
            (self.user_id, self.site_name, self.login_type)
        )
        exists = cursor.fetchone()
        if exists:
            print(f"ℹ️ Цей тип входу ({self.login_type}) для сайту {self.site_name} вже додано.")
        else:
            # Якщо login/password не передані, запитаємо у користувача
            if self.login is None:
                self.login = input("Введіть логін: ").strip()
            if self.password is None:
                self.password = input("Введіть пароль: ").strip()

            cursor.execute(
                "INSERT INTO site_credentials (user_id, site_name, login, password, login_type) "
                "VALUES (%s, %s, %s, %s, %s)",
                (self.user_id, self.site_name, self.login, self.password, self.login_type)
            )
            conn.commit()
            print(f"✅ Логін для {self.site_name} додано (тип: {self.login_type})")
        cursor.close()
        conn.close()

    @staticmethod
    def get_all(user_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT site_name, login, password, login_type FROM site_credentials WHERE user_id=%s",
            (user_id,)
        )
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
