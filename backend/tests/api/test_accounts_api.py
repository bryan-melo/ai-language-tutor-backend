import pytest

from main import app
from fastapi.testclient import TestClient


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
   
@pytest.fixture
def client():
   with TestClient(app) as c:
      yield c


class TestAccountAPI():
   # Test creating account with dummy data
   def test_create_account_pos(self, client, account_data):
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
      
   
   # Test creating an account with missing required fields (l_name, primary_lang)
   def test_create_account_neg(self, client):
      data = {
         "f_name": "Name",
         "email": "name@name.com",
         "username": "namename",
         "password": "name1234"
      }
      
      url = "/account/create/create-account"
      response = client.post(url, json=data)
      
      assert response.status_code == 422
      
   
   # Test login endpoint using valid credentials
   def test_login_with_valid_credentials(self, client, account_data):
      # Create test account
      create_account_url = "/account/create/create-account"
      create_account_response = client.post(create_account_url, json=account_data)
      
      # Verify create account status code
      assert create_account_response.status_code == 201
      
      # Prep data using fixture for login endpoint
      prep_data = {
         "username": account_data["username"],
         "password": account_data["password"]
      }
      
      login_url = "/account/login"
      login_response = client.post(login_url, json=prep_data)
      
      # Verify login status code
      assert login_response.status_code == 200
      
      # Check data integrity
      login_response_data = login_response.json()
      assert "id" in login_response_data
      assert login_response_data["f_name"] == "Test"
      assert login_response_data["l_name"] == "Dummy"
      assert login_response_data["email"] == "test.dummy@testing.com"
      assert login_response_data["username"] == "testdummy1234"
      assert login_response_data["primary_lang"] == "English"
      
      # Clean up by removing test account
      response = client.delete(f'/account/delete/delete-account/{login_response_data["id"]}')
      assert response.status_code == 200
      
   
   # Test login endpoint using invalid credentials
   def test_login_with_invalid_credentials(self, client):
      # Create dummy data
      data = {
         "username": "username",
         "password": "password"
      }
      
      url = "/account/login"
      response = client.post(url, json=data)
      
      assert response.status_code == 401
      
   
   # Test get all accounts
   
   
      
      
      
      
      
      
      
      
      
      
      
      
         
      
