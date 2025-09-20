import os
import pytest
from db.database import init_db, get_connection

TEST_DB = "test_users.db"

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Фікстура: створює тестову БД перед кожним тестом."""
    monkeypatch.setattr("db.database.DB_NAME", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_database_initialization():
    """Перевірка, що таблиця users створюється успішно"""
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None, "Таблиця 'users' не була створена"

def test_insert_and_select_user():
    """Перевірка, що можна вставити користувача без помилок"""
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                ("alice", "pass123", "alice@example.com"))
    conn.commit()
    cur.execute("SELECT username, email FROM users WHERE username = ?", ("alice",))
    user = cur.fetchone()
    conn.close()
    assert user == ("alice", "alice@example.com")
