import pytest
import httpx


@pytest.fixture
def get_data():
   return {"username": "test"}


def test_example(get_data):
   assert "username" in get_data
   

@pytest.fixture
def config():
   return {"db": "sqlite"}


@pytest.fixture
def db_connection(config):
   return connect(config["db"])