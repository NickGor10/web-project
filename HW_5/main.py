from db.database import init_db
from models.user import User

def main():
    init_db()
    while True:
        print("\n--- Меню ---")
        print("1 - Зареєструватися")
        print("2 - Увійти")
        print("3 - Вийти")
        choice = input("Оберіть опцію: ")

        if choice == "1":
            username = input("Введіть username: ")
            password = input("Введіть пароль: ")
            email = input("Введіть email: ")
            user = User(username, password, email)
            if user.register():
                print("✅ Користувач зареєстрований успішно!")
            else:
                print("❌ Помилка: такий username або email вже існує.")

        elif choice == "2":
            username = input("Username: ")
            password = input("Пароль: ")
            if User.login(username, password):
                print("✅ Успішний вхід!")
            else:
                print("❌ Неправильні дані!")

        elif choice == "3":
            print("👋 До побачення!")
            break
        else:
            print("⚠ Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
