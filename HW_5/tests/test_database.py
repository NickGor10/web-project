import pytest
from db.database import init_db, get_connection

@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """Перед кожним тестом створюємо таблицю, після — очищаємо."""
    init_db()
    yield
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()

def test_database_connection():
    """Перевірка підключення до MySQL"""
    conn = get_connection()
    assert conn.is_connected()
    conn.close()

def test_create_table():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'users'")
    assert cursor.fetchone() is not None
    conn.close()

def test_insert_and_select_user():
    """Перевірка вставки користувача та отримання його з MySQL"""
    conn = get_connection()
    cursor = conn.cursor()

    # Вставляємо тестового користувача
    cursor.execute(
        "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
        ("alice", "pass123", "alice@example.com")
    )
    conn.commit()

    # Отримуємо дані назад
    cursor.execute("SELECT username, email FROM users WHERE username = %s", ("alice",))
    user = cursor.fetchone()
    conn.close()

    assert user is not None
    assert user[0] == "alice"
    assert user[1] == "alice@example.com"

def test_insert_duplicate_user_fails():
    """Перевірка, що дубльовані username/email не додаються"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
        ("bob", "secret", "bob@example.com")
    )
    conn.commit()

    with pytest.raises(Exception):
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
            ("bob", "secret", "bob@example.com")
        )
        conn.commit()

    conn.close()
