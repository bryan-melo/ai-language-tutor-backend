import pytest

from main import app
from fastapi.testclient import TestClient


@pytest.fixture
def account_data():
   return [
      {
         "f_name": "test1",
         "l_name": "dummy1",
         "email": "test1@test.com",
         "username": "test1",
         "password": "test1",
         "primary_lang": "test"
      },
      {
         "f_name": "test2",
         "l_name": "dummy2",
         "email": "test2@test.com",
         "username": "test2",
         "password": "test2",
         "primary_lang": "test"
      },
      {
         "f_name": "test3",
         "l_name": "dummy3",
         "email": "test3@test.com",
         "username": "test3",
         "password": "test3",
         "primary_lang": "test"
      },
   ]
   
@pytest.fixture
def client():
   with TestClient(app) as c:
      yield c


class TestAccountAPI():
   # Test create account endpoint using complete data
   def test_create_account_pos(self, client, account_data):
      # Create account using fixture data
      url = "/account/create/create-account"
      response = client.post(url, json=account_data[0])
      assert response.status_code == 201  
      
      # Verify response structure using AccountRead pydanctic model
      data = response.json()
      assert "id" in data
      assert data["f_name"] == "test1"
      assert data["l_name"] == "dummy1"
      assert data["email"] == "test1@test.com"
      assert data["username"] == "test1"
      assert data["primary_lang"] == "test"
      
      # Clean up by removing test account
      response = client.delete(f'/account/delete/delete-account/{data["id"]}')
      assert response.status_code == 200
      
   
   # Test creating an account endpoint using incomplete data
   def test_create_account_neg(self, client):
      # Data with missing fields
      data = {
         "f_name": "Name",
         "email": "name@name.com",
         "username": "namename",
         "password": "name1234"
      }
      
      # Call create account endpoint and send bad data
      url = "/account/create/create-account"
      response = client.post(url, json=data)
      assert response.status_code == 422
      
   
   # Test login endpoint using valid credentials
   def test_login_with_valid_credentials(self, client, account_data):
      # Create test account
      create_account_url = "/account/create/create-account"
      create_account_response = client.post(create_account_url, json=account_data[0])
      assert create_account_response.status_code == 201
      
      # Prep data using fixture for login endpoint
      prep_data = {
         "username": account_data[0]["username"],
         "password": account_data[0]["password"]
      }
      
      # Send valid credentials to login endpoint
      login_url = "/account/login"
      login_response = client.post(login_url, json=prep_data)
      assert login_response.status_code == 200
      
      # Check data integrity
      login_response_data = login_response.json()
      assert "id" in login_response_data
      assert login_response_data["f_name"] == "test1"
      assert login_response_data["l_name"] == "dummy1"
      assert login_response_data["email"] == "test1@test.com"
      assert login_response_data["username"] == "test1"
      assert login_response_data["primary_lang"] == "test"
      
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
      
      # Send dummy data to login endpoint
      url = "/account/login"
      response = client.post(url, json=data)
      assert response.status_code == 401
      
   
   # Test get all accounts
   def test_get_all_accounts(self, client, account_data):
      # Create test account
      create_account_url = "/account/create/create-account"
      for account in account_data:
         create_account_response = client.post(create_account_url, json=account)
         assert create_account_response.status_code == 201

      # Get all accounts
      response = client.get("/account/get-all-accounts")
      assert response.status_code == 200
      
      # Check response data 
      accounts = response.json()
      for account in accounts:
         assert "id" in account
         assert "test" in account["f_name"]
         assert "test" in account["l_name"]
         assert "@test.com" in account["email"]
         assert "test" in account["username"]
         assert "test" in account["primary_lang"]
         
      # Delete test accounts, clean up
      for account in accounts:
         delete_response = client.delete(f'/account/delete/delete-account/{account["id"]}')
         assert delete_response.status_code == 200
