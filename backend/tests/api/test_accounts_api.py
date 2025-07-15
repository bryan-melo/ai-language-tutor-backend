import pytest

from main import app
from fastapi.testclient import TestClient

# API URLS constants
CREATE_ACCOUNT_URL = "/account/create/create-account"
LOGIN_URL = "/account/login"
GET_ALL_ACCOUNTS_URL = "/account/get-all-accounts"
GET_ACCOUNT_URL = "/account/get-account/"
DELETE_ACCOUNT_URL = "/account/delete/delete-account/"


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
   # Test create account endpoint
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("John", "Doe", "johndoe@gmail.com", "johndoe", "password", "english", 201),  # positive test case
      ("Peter", "Jackson", "peterjackson@gmail.com", "peterjackson", "password", "english", 201), # positive test case
      ("Bobby", None, None, "bobbyjones", "english", "password", 422),   # negative test case
      (None, None, None, None, None, None, 422) # negative test case
   ])
   def test_create_account_route(self, client, f_name, l_name, email, username, password, primary_lang, status_code):
      account_data = {
         "f_name": f_name,
         "l_name": l_name,
         "email": email,
         "username": username,
         "password": password,
         "primary_lang": primary_lang
      }
      # Create account using fixture data
      response = client.post(CREATE_ACCOUNT_URL, json=account_data)
      assert response.status_code == status_code
      
      if status_code != 201:
         return
      
      # Verify response structure using AccountRead pydanctic model
      data = response.json()
      assert "id" in data
      assert data["f_name"] == account_data["f_name"]
      assert data["l_name"] == account_data["l_name"]
      assert data["email"] == account_data["email"]
      assert data["username"] == account_data["username"]
      assert data["primary_lang"] == account_data["primary_lang"]
      
      # Clean up by removing test account
      response = client.delete(DELETE_ACCOUNT_URL + str(data["id"]))
      assert response.status_code == 204
      
      
   # Test login endpoint using valid credentials
   def test_login_with_valid_credentials(self, client, account_data):
      # Create test account
      create_account_response = client.post(CREATE_ACCOUNT_URL, json=account_data[0])
      assert create_account_response.status_code == 201
      
      # Prep data using fixture for login endpoint
      prep_data = {
         "username": account_data[0]["username"],
         "password": account_data[0]["password"]
      }
      
      # Send valid credentials to login endpoint
      login_response = client.post(LOGIN_URL, json=prep_data)
      assert login_response.status_code == 200
      
      # Check data integrity
      login_response_data = login_response.json()
      assert "id" in login_response_data
      assert login_response_data["f_name"] == account_data[0]["f_name"]
      assert login_response_data["l_name"] == account_data[0]["l_name"]
      assert login_response_data["email"] == account_data[0]["email"]
      assert login_response_data["username"] == account_data[0]["username"]
      assert login_response_data["primary_lang"] == account_data[0]["primary_lang"]
      
      # Clean up by removing test account
      response = client.delete(DELETE_ACCOUNT_URL + str(login_response_data["id"]))
      assert response.status_code == 204
      assert response.text == ""
      
   
   # Test login endpoint using invalid credentials
   def test_login_with_invalid_credentials(self, client):
      # Create dummy data
      data = {
         "username": "username",
         "password": "password"
      }
      
      # Send dummy data to login endpoint
      response = client.post(LOGIN_URL, json=data)
      assert response.status_code == 401
      
   
   # Test get all accounts
   def test_get_all_accounts(self, client, account_data):
      # Create test account
      for account in account_data:
         create_account_response = client.post(CREATE_ACCOUNT_URL, json=account)
         assert create_account_response.status_code == 201

      # Get all accounts
      response = client.get(GET_ALL_ACCOUNTS_URL)
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
         delete_response = client.delete(DELETE_ACCOUNT_URL + str(account["id"]))
         assert delete_response.status_code == 204


   # Test get all accounts with an empty DB
   def test_get_all_accounts_with_no_data(self, client):
      # Get all accounts
      accounts_response = client.get(GET_ALL_ACCOUNTS_URL)
      assert accounts_response.status_code == 200
      assert not accounts_response.json()
      
   
   # Test to get an account given the account_id
   def test_get_account_pos(self, client, account_data):
      # Create test account
      create_account_response = client.post(CREATE_ACCOUNT_URL, json=account_data[0])
      assert create_account_response.status_code == 201
      
      # Get accound by id
      account = create_account_response.json()
      get_account_response = client.get(GET_ACCOUNT_URL + str(account["id"]))
      assert get_account_response.status_code == 200
      
      # Verify data
      response_data = get_account_response.json()
      assert "id" in response_data
      assert response_data["f_name"] == account_data[0]["f_name"]
      assert response_data["l_name"] == account_data[0]["l_name"]
      assert response_data["email"] == account_data[0]["email"]
      assert response_data["username"] == account_data[0]["username"]
      assert response_data["primary_lang"] == account_data[0]["primary_lang"]
      
      # Remove account, clean up
      removed_account_response = client.delete(DELETE_ACCOUNT_URL + str(response_data["id"]))
      assert removed_account_response.status_code == 204
      
      
'''
Need to create fixture for deleting account
Need fixture for creating an account
'''