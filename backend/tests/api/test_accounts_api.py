import pytest
import random

from main import app
from fastapi import status
from fastapi.testclient import TestClient

# API URLS constants
CREATE_ACCOUNT_URL = "/account/create/create-account"
LOGIN_URL = "/account/login"
GET_ALL_ACCOUNTS_URL = "/account/get-all-accounts"
GET_ACCOUNT_URL = "/account/get-account/"
DELETE_ACCOUNT_URL = "/account/delete/delete-account/"

   
@pytest.fixture
def client():
   with TestClient(app) as c:
      yield c


class TestAccountAPI():
   # Test create account endpoint
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("John", "Doe", "johndoe@gmail.com", "johndoe", "password", "english", status.HTTP_201_CREATED),  # positive test 
      ("Peter", "Jackson", "peterjackson@gmail.com", "peterjackson", "password", "english", status.HTTP_201_CREATED), # positive test 
      ("Bobby", None, None, "bobbyjones", "english", "password", status.HTTP_422_UNPROCESSABLE_ENTITY),   # negative test 
      (None, None, None, None, None, None, status.HTTP_422_UNPROCESSABLE_ENTITY) # negative test 
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
      if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY:
         return
      
      # Verify response structure using AccountRead pydanctic model
      data = response.json()
      assert "id" in data
      assert data["f_name"] == f_name
      assert data["l_name"] == l_name
      assert data["email"] == email
      assert data["username"] == username
      assert data["primary_lang"] == primary_lang
      
      # Cleanup test accounts
      delete_account_helper(client, data["id"])
      

   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("John", "Doe", "johndoe@gmail.com", "johndoe", "johndoe", "english", status.HTTP_200_OK),    # positive test 
      ("Timothy", "Roe", "timothyroes@gmail.com", "timothyroe", "password", "english", status.HTTP_200_OK),   # positive test 
      (None, None, None, "johndoe", "johndoe", None, status.HTTP_401_UNAUTHORIZED),     # negative test 
      (None, None, None, "timothyroe", "password1234", None, status.HTTP_401_UNAUTHORIZED)     # negative test 
   ])
   # Test login endpoint using valid credentials
   def test_login_route(self, client, f_name, l_name, email, username, password, primary_lang, status_code):
      # Skip account creation for negative test cases (invalid credentials)
      if status_code == status.HTTP_200_OK:
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
         assert create_account_response.status_code == status.HTTP_201_CREATED
      
      # Prep data using fixture for login endpoint
      login_data = {
         "username": username,
         "password": password
      }
      
      # Send valid credentials to login endpoint
      login_response = client.post(LOGIN_URL, json=login_data)
      assert login_response.status_code == status_code
      
      
      if status_code == status.HTTP_401_UNAUTHORIZED:
         error_data = login_response.json()
         assert "detail" in error_data
         assert error_data["detail"] == "Invalid credentials"
         return
      
      # Check data integrity
      login_response_data = login_response.json()
      assert "id" in login_response_data
      assert login_response_data["f_name"] == f_name
      assert login_response_data["l_name"] == l_name
      assert login_response_data["email"] == email
      assert login_response_data["username"] == username
      assert login_response_data["primary_lang"] == primary_lang
      
      # Cleanup test accounts
      delete_account_helper(client, login_response_data["id"])
      
      
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("test1", "test1", "test1@test.com", "test1", "test1", "english", status.HTTP_200_OK),   # positive test 
      ("test2", "test2", "test2@test.com", "test2", "test2", "english", status.HTTP_200_OK),   # positive test
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND),   # negative test
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND)    # negative test
   ])
   # Test to get an account given the account_id
   def test_get_account_route(self, client, f_name, l_name, email, username, password, primary_lang, status_code):
      # Create test accounts for inputs with valid credentials
      if status_code == status.HTTP_200_OK:
         account_data = {
            "f_name": f_name,
            "l_name": l_name,
            "email": email,
            "username": username,
            "password": password,
            "primary_lang": primary_lang
         }
         create_account_response = client.post(CREATE_ACCOUNT_URL, json=account_data)
         assert create_account_response.status_code == status.HTTP_201_CREATED
      
         # Test get account route with given credentials
         account = create_account_response.json()
      else:
         # For negative test cases, test with random 
         random_num = random.randint(-100000, -1)
         account = {"id": random_num}
         
      get_account_response = client.get(f"{GET_ACCOUNT_URL}{account['id']}")
      assert get_account_response.status_code == status_code
      
      if status_code == status.HTTP_404_NOT_FOUND:
         error_data = get_account_response.json()
         assert "detail" in error_data
         assert error_data["detail"] == "Account not found"
         return
      
      # Verify data
      response_data = get_account_response.json()
      assert "id" in response_data
      assert response_data["f_name"] == f_name
      assert response_data["l_name"] == l_name
      assert response_data["email"] == email
      assert response_data["username"] == username
      assert response_data["primary_lang"] == primary_lang
      
      # Cleanup test account
      delete_account_helper(client, response_data["id"])
      
      
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
         assert create_account_response.status_code == status.HTTP_201_CREATED

      # Fetch all accounts
      response = client.get(GET_ALL_ACCOUNTS_URL)
      assert response.status_code == status.HTTP_200_OK
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
         delete_account_helper(client, account["id"])


def delete_account_helper(client, account_id):
    response = client.delete(f"{DELETE_ACCOUNT_URL}{account_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert response.text == ""