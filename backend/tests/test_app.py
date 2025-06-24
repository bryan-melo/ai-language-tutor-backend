from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_root():
   assert 1 + 1 == 2
 

