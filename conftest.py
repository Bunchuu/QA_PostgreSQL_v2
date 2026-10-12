import psycopg2
import pytest

# DB parameters defined in docker-compose.yml
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "bunchuu_db",
    "user": "bunchuu",
    "password": "bunchuu"
}


@pytest.fixture(scope="session")
def db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    yield conn
    conn.close()


@pytest.fixture
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()
    db_connection.rollback()