import pytest
from db.database import init_db, get_connection
from models.user import User

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Фікстура: створює чисту БД перед кожним тестом."""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    yield
    # після тесту ще раз чистимо, щоб уникнути конфліктів між тестами
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def test_register_user_and_duplicate_username():
    """Реєстрація користувача та перевірка, що дубль username не проходить."""
    user = User("testuser", "12345", "test@example.com")
    assert user.register() is True
    # Повторна реєстрація того самого username/email має повернути False
    assert user.register() is False
    assert User.login("testuser", "12345") is True
    assert User.login("testuser", "wrongpass") is False
    assert User.login("unknown", "12345") is False

def test_register_user_invalid_email():
    """Спроба зареєструвати користувача з невалідним email — має підняти ValueError."""
    # bad = User("baduser", "12345", "not_an_email")
    # with pytest.raises(ValueError):
    #     bad.register()
    with pytest.raises(ValueError):
        User("baduser", "12345", "not_an_email")

def test_duplicate_email_blocked():
    """Перевірка, що два різні username з однаковим email не пройдуть другу реєстрацію."""
    user1 = User("alice", "pw1", "same@example.com")
    user2 = User("bob", "pw2", "same@example.com")
    assert user1.register() is True
    assert user2.register() is False

def test_login_success_and_fail():
    """Успішний логін, логін з неправильним паролем і логін неіснуючого користувача."""
    user = User("john", "pass123", "john@example.com")
    user.register()
    assert User.login("john", "pass123") is True
    assert User.login("john", "wrongpass") is False
    assert User.login("unknown", "pass123") is False

def test_whitespace_and_case_insensitive_login():
    """Перевірка, що login працює незалежно від регістру та зайвих пробілів."""
    user = User("caseuser", "secret", "case@example.com")
    user.register()
    assert User.login("  CaseUser  ", "secret") is True  # ігноруємо пробіли та регістр
