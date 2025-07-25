import pytest
import random

from typing import Any
from fastapi import status
from fastapi.testclient import TestClient

# Local file
from backend.main import app 
from backend.app.models.account_models import AccountCreate
from backend.app.models.account_models import LoginRequest
from .utils import validate_and_create_instance, delete_instance

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
   # <---------------------------->
   #   Account API Endpoint Tests
   # <---------------------------->
   @pytest.mark.parametrize("account_data, status_code", [
      ({"f_name": "John", "l_name": "Doe", "email": "johndoe@gmail.com", "username": "johndoe", "password": "password", "primary_lang": "English"}, status.HTTP_201_CREATED),
      ({"f_name": "Peter", "l_name": "Jackson", "email": "peterjackson@gmail.com", "username": "peterjackson", "password": "password", "primary_lang": "English"}, status.HTTP_201_CREATED),
      ({"f_name": "Bobby", "l_name": "Matthew", "email": "bobbymatthrew@gmail.com", "username": "Bobby", "password": "Bobby", "primary_lang": "japanese"}, status.HTTP_422_UNPROCESSABLE_ENTITY),
      ({"f_name": None, "l_name": None, "email": None, "username": None, "password": None, "primary_lang": None}, status.HTTP_422_UNPROCESSABLE_ENTITY),
   ])
   def test_create_account_route(self, client: TestClient, account_data: dict[str, Any], status_code: int):
      """
      Tests account creation with valid and invalid inputs. 
      Valid accounts are verified and deleted after creation.

      - Expects 201 for valid input with all required fields
      - Expects 422 for missing or invalid fields
      """
      # Validate input data using Pydantic model before sending request
      response_data = validate_and_create_instance(client, AccountCreate, account_data, status_code, CREATE_ACCOUNT_URL)
      
      # End test early for expected failure
      if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY or not response_data:
         return
       
      # Validate fields match expected values
      self.validate_account(
         response_data,    
         account_data["f_name"],
         account_data["l_name"],    
         account_data["email"], 
         account_data["username"], 
         account_data["primary_lang"]
      )
            
      # Clean up test account
      delete_instance(client, response_data["id"], DELETE_ACCOUNT_URL)


   @pytest.mark.parametrize("account_data, status_code", [
      ({"f_name": "John", "l_name": "Doe", "email": "johndoe@gmail.com", "username": "johndoe", "password": "password", "primary_lang": "English"}, status.HTTP_200_OK),
      ({"f_name": "Timothy", "l_name": "Roe", "email": "timothyroes@gmail.com", "username": "timothyroe", "password": "password", "primary_lang": "English"}, status.HTTP_200_OK),
      ({"f_name": None, "l_name": None, "email": None, "username": "johndoe", "password": "johndoe", "primary_lang": None}, status.HTTP_401_UNAUTHORIZED),
      ({"f_name": None, "l_name": None, "email": None, "username": "timothyroe", "password": "password1234", "primary_lang": None}, status.HTTP_401_UNAUTHORIZED),
   ])
   def test_login_route(self, client: TestClient, account_data: dict[str, Any], status_code: int):
      """
      Tests account login with valid and invalid credentials.
      Valid logins are verified, and test accounts are cleaned up afterward.

      - Expects 200 for correct username and password
      - Expects 401 for incorrect or missing credentials
      """
      if status_code == status.HTTP_200_OK:
         _ = validate_and_create_instance(client, AccountCreate, account_data, status.HTTP_201_CREATED, CREATE_ACCOUNT_URL)
            
      # Prepare login payload
      login_data = {
         "username": account_data["username"],
         "password": account_data["password"]
      }

      validated_login = LoginRequest.model_validate(login_data)
      assert isinstance(validated_login, LoginRequest), f"Expected LoginRequest instance, got {type(validated_login)}"

      # Make login request
      login_response = client.post(LOGIN_URL, json=login_data)
      assert login_response.status_code == status_code, f"Expected {status_code}, got {login_response.status_code}"

      if status_code == status.HTTP_401_UNAUTHORIZED:
         error_data = login_response.json()
         assert "detail" in error_data, "Missing 'detail' in error response"
         assert error_data["detail"] == "Invalid credentials", f"Unexpected error message: {error_data['detail']}"
         return

      # Validate account data from login response
      login_response_data = login_response.json()
      self.validate_account(
         login_response_data,
         account_data["f_name"],
         account_data["l_name"],
         account_data["email"],
         account_data["username"],
         account_data["primary_lang"]
      )

      # Clean up test account
      delete_instance(client, login_response_data["id"], DELETE_ACCOUNT_URL)
   

   @pytest.mark.parametrize("account_data, status_code", [
      ({"f_name": "test1", "l_name": "test1", "email": "test1@gmail.com", "username": "test1", "password": "test1", "primary_lang": "English"}, status.HTTP_200_OK),
      ({"f_name": "test2", "l_name": "test2", "email": "test2@gmail.com", "username": "test2", "password": "test2", "primary_lang": "English"}, status.HTTP_200_OK),
      (None, status.HTTP_404_NOT_FOUND),  
      (None, status.HTTP_404_NOT_FOUND)   # negative test -- different int generated
   ])
   def test_get_account_route(self, client: TestClient, account_data: dict[str, Any], status_code: int):
      """
      Tests retrieving an account by ID with both valid and invalid scenarios.
      Valid accounts are verified against expected values and deleted after the test.

      - Expects 200 for existing accounts with valid IDs
      - Expects 404 for non-existent account IDs
      """
      if status_code == status.HTTP_200_OK:
         created_account = validate_and_create_instance(client, AccountCreate, account_data, status.HTTP_201_CREATED, CREATE_ACCOUNT_URL)
         account_id = created_account["id"]
      else:
         account_id = random.randint(-100000, -1)

      response = client.get(f"{GET_ACCOUNT_URL}{account_id}")
      assert response.status_code == status_code, f"Expected status {status_code}, got {response.status_code}"

      if status_code == status.HTTP_404_NOT_FOUND:
         error_data = response.json()
         assert "detail" in error_data, "Missing 'detail' in error response"
         assert error_data["detail"] == "Account not found", f"Unexpected detail message: {error_data['detail']}"
         return

      fetched_account = response.json()
      self.validate_account(
         fetched_account,
         account_data["f_name"],
         account_data["l_name"],
         account_data["email"],
         account_data["username"],
         account_data["primary_lang"]
      )

      delete_instance(client, account_id, DELETE_ACCOUNT_URL)
      
      
   def test_get_all_accounts_route(self, client: TestClient):
      """
      Tests retrieval of all accounts and validates presence of test entries.

      - Creates multiple test accounts
      - Expects 200 response from the get-all endpoint
      - Verifies all test accounts are returned with correct values
      - Cleans up all created test accounts after verification
      """
      # Create multiple test accounts
      test_accounts = [
         {
               "f_name": f"test{i}",
               "l_name": f"test{i}",
               "email": f"test{i}@test.com",
               "username": f"test{i}",
               "password": f"test{i}",
               "primary_lang": "English"
         }
         for i in range(1, 5)
      ]

      # Create test accounts in database and validate instance
      for account_data in test_accounts:
         _ = validate_and_create_instance(client, AccountCreate, account_data, status.HTTP_201_CREATED, CREATE_ACCOUNT_URL)

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
         delete_instance(client, account["id"], DELETE_ACCOUNT_URL)
         
   
   @pytest.mark.parametrize("account_data, status_code", [
      ({"f_name": "test1", "l_name": "test1", "email": "test1@test.com", "username": "test1", "password": "test1", "primary_lang": "English"}, status.HTTP_204_NO_CONTENT),
      ({"f_name": "test2", "l_name": "test2", "email": "test2@test.com", "username": "test2", "password": "test2", "primary_lang": "English"}, status.HTTP_204_NO_CONTENT),
      (None, status.HTTP_404_NOT_FOUND),
      (None, status.HTTP_404_NOT_FOUND),
   ]) 
   def test_delete_account_route(self, client: TestClient, account_data: dict[str, Any], status_code: int):
      """
      Tests account deletion with valid and invalid account IDs.

      - Expects 204 when deleting an existing account
      - Expects 404 when account ID is not found

      Valid accounts are created before deletion and verified.
      """
      if status_code == status.HTTP_204_NO_CONTENT:
         account = validate_and_create_instance(client, AccountCreate, account_data, status.HTTP_201_CREATED, CREATE_ACCOUNT_URL)
         self.validate_account(
            account, 
            account_data["f_name"],
            account_data["l_name"],
            account_data["email"],
            account_data["username"],
            account_data["primary_lang"]
         )
      else:
         # For negative test cases, test with random ID
         random_num = random.randint(-100000, -1)
         account = {"id": random_num}

      response = client.delete(f"{DELETE_ACCOUNT_URL}{account['id']}")
      assert response.status_code == status_code, f"Expected status {status_code}, got {response.status_code}"

      if status_code == status.HTTP_404_NOT_FOUND:
         error_data = response.json()
         assert "detail" in error_data
         assert error_data["detail"] == "Account not found"
         return
      
      
   # <------------------>
   #   Helper functions
   # <------------------>   
   def validate_account(self, account: dict[str, Any], f_name: str, l_name: str, email: str, username: str, primary_lang: str) -> None:
      """
      Helper function to verify the structure and content of an account object.

      - Asserts presence of required keys
      - Asserts field values match expected input
      """
      assert account['id'] is not None, "Expected account.id to be populated"
      assert account['f_name'] == f_name, f"Expected f_name={f_name}, got {account['f_name']}"
      assert account['l_name'] == l_name, f"Expected l_name={l_name}, got {account['l_name']}"
      assert account['email'] == email, f"Expected email={email}, got {account['email']}"
      assert account['username'] == username, f"Expected username={username}, got {account['username']}"
      assert account['primary_lang'] == primary_lang, f"Expected primary_lang={primary_lang}, got {account['primary_lang']}"
