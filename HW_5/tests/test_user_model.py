import os
import pytest
from db.database import init_db, get_connection
from models.user import User

TEST_DB = "test_users.db"

@pytest.fixture(autouse=True)
def setup_and_teardown_db(monkeypatch):
    """
    Фікстура для тестової бази:
    - підмінює ім'я БД на TEST_DB
    - видаляє файл перед тестом і після тесту
    - ініціалізує схему
    """
    # підмінюємо назву БД у модулі db.database
    monkeypatch.setattr("db.database.DB_NAME", TEST_DB)
    # видаляємо стару тестову базу, якщо є
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    # створюємо свіжу бд зі схемою
    init_db()
    yield
    # чистимо після тесту
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_register_user_and_duplicate_username():
    """Реєстрація користувача та перевірка, що дубль username не проходить."""
    user = User("testuser", "12345", "test@example.com")
    assert user.register() is True
    # Повторна реєстрація того самого username/email має повернути False (IntegrityError)
    assert user.register() is False

def test_register_user_invalid_email():
    """Спроба зареєструвати користувача з невалідним email — має підняти ValueError."""
    bad = User("baduser", "12345", "not_an_email")
    with pytest.raises(ValueError):
        bad.register()

def test_duplicate_email_blocked():
    """Перевірка, що два різні username з однаковим email не пройдуть другий реєстрації."""
    user1 = User("alice", "pw1", "same@example.com")
    user2 = User("bob", "pw2", "same@example.com")
    assert user1.register() is True
    # друга реєстрація з тим же email має впасти (повернути False)
    assert user2.register() is False

def test_login_success_and_fail():
    """Успішний логін, логін з неправильним паролем і логін неіснуючого користувача."""
    user = User("john", "pass123", "john@example.com")
    user.register()
    assert User.login("john", "pass123") is True
    assert User.login("john", "wrongpass") is False
    assert User.login("unknown", "pass123") is False
