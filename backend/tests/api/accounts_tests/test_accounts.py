import pytest
import httpx


@pytest.fixture
def get_data_example():
   return {"username": "test"}


def test_example(get_data):
   assert "username" in get_data_example

