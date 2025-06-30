import pytest
import httpx


@pytest.fixture
def get_data():
   return {"username": "test"}


@pytest.fixture
def db_connection():
   conn = connect_to_db()
   yield conn
   conn.close()

def test_example(get_data):
   assert "username" in get_data
   

