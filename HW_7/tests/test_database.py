import pytest
import os
from db.database import init_db, get_connection

TEST_DB = "test_products.db"

@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    """Фікстура для тестової БД SQLite."""
    monkeypatch.setattr("db.database", "DB_NAME", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    init_db()
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

def test_table_creation():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
    table = cursor.fetchone()
    conn.close()
    assert table is not None

def test_insert_and_select():
    from db.models import Product
    product = Product("iPhone 14", "30000", "/prod1", "4.5")
    product.save()
    products = Product.get_all()
    assert len(products) == 1
    assert products[0][0] == "iPhone 14"
