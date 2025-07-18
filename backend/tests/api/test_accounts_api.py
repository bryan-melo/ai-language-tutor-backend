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
         "f_name": "test10",
         "l_name": "dummy10",
         "email": "test10@test.com",
         "username": "test10",
         "password": "test10",
         "primary_lang": "test"
      },
      {
         "f_name": "test20",
         "l_name": "dummy20",
         "email": "test20@test.com",
         "username": "test20",
         "password": "test20",
         "primary_lang": "test"
      },
      {
         "f_name": "test30",
         "l_name": "dummy30",
         "email": "test30@test.com",
         "username": "test30",
         "password": "test30",
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
      
      # End test here for negative test cases
      if status_code != 201:
         return
      
      # Verify response structure using AccountRead pydanctic model
      data = response.json()
      assert "id" in data
      assert data["f_name"] == f_name
      assert data["l_name"] == l_name
      assert data["email"] == email
      assert data["username"] == username
      assert data["primary_lang"] == primary_lang
      
      # Clean up by removing test account
      response = client.delete(DELETE_ACCOUNT_URL + str(data["id"]))
      assert response.status_code == 204
      assert response.text == ""
      

   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, login_status_code", [
      ("John12", "Doe12", "johndoe12@gmail.com", "johndoe12", "password12", "english", 200),
      ("Timothy12", "Roe12", "timothyroes12@gmail.com", "timothyroe12", "password12", "english", 200),
      #("John", "Doe", "johndoe@gmail.com", "johndoe", None, "english", 422),
   ])
   # Test login endpoint using valid credentials
   def test_login_route(self, client, f_name, l_name, email, username, password, primary_lang, login_status_code):
      account_data = {
         "f_name": f_name,
         "l_name": l_name,
         "email": email,
         "username": username,
         "password": password,
         "primary_lang": primary_lang
      }
      
      # Create test account
      create_account_response = client.post(CREATE_ACCOUNT_URL, json=account_data)
      assert create_account_response.status_code == 201
      
      # Prep data using fixture for login endpoint
      login_data = {
         "username": username,
         "password": password
      }
      
      # Send valid credentials to login endpoint
      login_response = client.post(LOGIN_URL, json=login_data)
      assert login_response.status_code == login_status_code
      
      # End test here for negative test cases
      if login_status_code != 200:
         return
      
      # Check data integrity
      login_response_data = login_response.json()
      assert "id" in login_response_data
      assert login_response_data["f_name"] == f_name
      assert login_response_data["l_name"] == l_name
      assert login_response_data["email"] == email
      assert login_response_data["username"] == username
      assert login_response_data["primary_lang"] == primary_lang
      
      # Clean up by removing test account
      response = client.delete(DELETE_ACCOUNT_URL + str(login_response_data["id"]))
      assert response.status_code == 204
      assert response.text == ""
      
      
   # Test to get an account given the account_id
   def test_get_account_route(self, client, account_data):
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
      assert removed_account_response.text == ""
      
      
   # Test get all accounts
   def test_get_all_accounts_route(self, client):
      # Create multiple test accounts
      test_accounts = [
         {
               "f_name": f"test{i}",
               "l_name": f"test{i}",
               "email": f"test{i}@test.com",
               "username": f"test{i}",
               "password": f"test{i}",
               "primary_lang": "english"
         }
         for i in range(1, 5)
      ]

      for account in test_accounts:
         create_account_response = client.post(CREATE_ACCOUNT_URL, json=account)
         assert create_account_response.status_code == 201

      # Fetch all accounts
      response = client.get(GET_ALL_ACCOUNTS_URL)
      assert response.status_code == 200
      accounts = response.json()

      # Filter only test accounts
      test_entries = [account for account in accounts if account["f_name"].startswith("test")]

      # Validate each test entry
      for i, account in enumerate(test_entries):
         assert account["f_name"] == test_accounts[i]["f_name"]
         assert account["l_name"] == test_accounts[i]["l_name"]
         assert account["email"] == test_accounts[i]["email"]
         assert account["username"] == test_accounts[i]["username"]
         assert account["primary_lang"] == test_accounts[i]["primary_lang"]

      # Cleanup test accounts
      for account in test_entries:
         delete_response = client.delete(f"{DELETE_ACCOUNT_URL}{account['id']}")
         assert delete_response.status_code == 204
         assert delete_response.text == ""
      
      
'''
   - Implement test for test a single account using mark.parametrize
   - Login route needs negative test cases
   - Needs fixing: Create account currently allows Null or None to be passed into the DB, causing issues 
   when using get all accounts route
'''