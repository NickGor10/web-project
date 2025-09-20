import pytest
from db.database import init_db, get_connection
from models.user import User
from models.site_credential import SiteCredential


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    init_db()
    # Очистимо таблиці перед тестами
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM site_credentials")
    cursor.execute("DELETE FROM users")
    conn.commit()
    conn.close()


def test_add_and_retrieve_site_credential():
    user = User("alice", "password", "alice@example.com")
    user.register()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username=%s", ("alice",))
    user_id = cursor.fetchone()[0]
    cursor.close()
    conn.close()

    cred = SiteCredential(user_id, "Google", "alice@gmail.com", "secret123", "google")
    cred.add()

    records = SiteCredential.get_all(user_id)
    assert len(records) == 1
    assert records[0][0] == "Google"
    assert records[0][1] == "alice@gmail.com"
    assert records[0][3] == "google"
