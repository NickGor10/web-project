from models.user import User
from models.site_credential import SiteCredential


def main():
    print("=== Система управління користувачами та логінами на сайтах ===")

    current_user = None

    while True:
        if current_user is None:
            print("\nВиберіть опцію:")
            print("1 - Зареєструватися")
            print("2 - Увійти")
            print("3 - Вийти")
            choice = input(">>> ").strip()

            if choice == "1":
                username = input("Введіть username: ").strip()
                password = input("Введіть password: ").strip()
                email = input("Введіть email: ").strip()

                try:
                    user = User(username, password, email)
                    if user.register():
                        print(f"✅ Користувач {username} успішно зареєстрований!")
                    else:
                        print(f"❌ Користувач з таким username або email вже існує.")
                except ValueError as e:
                    print(e)

            elif choice == "2":
                username = input("Введіть username: ").strip()
                password = input("Введіть password: ").strip()
                if User.login(username, password):
                    print("✅ Успішний вхід!")
                    current_user = username
                else:
                    print("❌ Неправильні дані!")

            elif choice == "3":
                print("Вихід із програми...")
                break

            else:
                print("❌ Невірна опція, спробуйте ще раз.")

        else:
            print(f"\nЛаскаво просимо, {current_user}!")
            print("Виберіть опцію:")
            print("1 - Додати логін на сайт")
            print("2 - Переглянути всі логіни")
            print("3 - Вийти (Logout)")
            choice = input(">>> ").strip()

            if choice == "1":
                site_name = input("Назва сайту: ").strip()
                login_type = input("Тип входу (google/apple/facebook/other) [other]: ").strip().lower()
                if login_type not in ("google", "apple", "facebook"):
                    login_type = "other"

                # Отримуємо user_id
                from db.database import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username=%s", (current_user,))
                user_id = cursor.fetchone()[0]
                cursor.close()
                conn.close()

                # Перевіряємо, чи site + user_id + login_type вже є
                from models.site_credential import SiteCredential
                cred = SiteCredential(user_id, site_name)
                cred.login_type = login_type
                cred.add()  # всередині add() перевірка, чи потрібен login/password



            elif choice == "2":
                from db.database import get_connection
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("SELECT id FROM users WHERE username=%s", (current_user,))
                user_id = cursor.fetchone()[0]
                cursor.close()
                conn.close()

                credentials = SiteCredential.get_all(user_id)
                if not credentials:
                    print("ℹ️ Немає доданих логінів.")
                else:
                    print("\nВаші логіни на сайтах:")
                    for site_name, login, password, login_type in credentials:
                        print(f"- {site_name} | {login} | {password} | тип: {login_type}")

            elif choice == "3":
                print(f"Вихід користувача {current_user}")
                current_user = None
            else:
                print("❌ Невірна опція, спробуйте ще раз.")


if __name__ == "__main__":
    main()
