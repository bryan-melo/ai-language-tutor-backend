import pytest

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.fixture
def account_data():
   return {
      "f_name": "Test",
      "l_name": "Dummy",
      "email": "test.dummy@testing.com",
      "username": "testdummy1234",
      "password": "test1234",
      "primary_lang": "English"
   }


class TestAccountAPI():
   # Test creating account with dummy data
   def test_create_account(self, account_data):
      url = "/account/create/create-account"
      response = client.post(url, json=account_data)
      
      # Verify status code
      assert response.status_code == 201  
      
      # Verify response structure using AccountRead pydanctic model
      data = response.json()
      assert "id" in data
      assert data["f_name"] == "Test"
      assert data["l_name"] == "Dummy"
      assert data["email"] == "test.dummy@testing.com"
      assert data["username"] == "testdummy1234"
      assert data["primary_lang"] == "English"
      
      # Clean up by removing test account
      response = client.delete(f'/account/delete/delete-account/{data["id"]}')
      assert response.status_code == 200
      
      
      
      
      
         
      
