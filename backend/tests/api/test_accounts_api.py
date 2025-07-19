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
   # <---------------------------->
   #   Account API Endpoint Tests
   # <---------------------------->
   """
   Tests account creation with valid and invalid inputs.

   - Expects 201 for valid input with all required fields
   - Expects 422 for missing or invalid fields

   Valid accounts are verified and deleted after creation.
   """
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
      # Create account, validate status code, and get the response data
      account_data = self.create_account(client, account_data, status_code)
      
      # End test here for negative test cases
      if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY or not account_data:
         return
      
      # Validate account data
      self.validate_account(account_data, f_name, l_name, email, username, primary_lang)
            
      # Cleanup test accounts
      self.delete_account(client, account_data["id"])
      

   """
   Tests account login with valid and invalid credentials.

   - Expects 200 for correct username and password
   - Expects 401 for incorrect or missing credentials

   Valid logins are verified, and test accounts are cleaned up afterward.
   """
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("John", "Doe", "johndoe@gmail.com", "johndoe", "johndoe", "english", status.HTTP_200_OK),    # positive test 
      ("Timothy", "Roe", "timothyroes@gmail.com", "timothyroe", "password", "english", status.HTTP_200_OK),   # positive test 
      (None, None, None, "johndoe", "johndoe", None, status.HTTP_401_UNAUTHORIZED),     # negative test 
      (None, None, None, "timothyroe", "password1234", None, status.HTTP_401_UNAUTHORIZED)     # negative test 
   ])
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
         # Create account, validate status code, and get the response data
         self.create_account(client, account_data, status.HTTP_201_CREATED)

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
      
      # Validate account data
      account_data = login_response.json()
      self.validate_account(account_data, f_name, l_name, email, username, primary_lang)
      
      # Cleanup test accounts
      self.delete_account(client, account_data["id"])
      
      
   """
   Tests retrieving an account by ID with both valid and invalid scenarios.

   - Expects 200 for existing accounts with valid IDs
   - Expects 404 for non-existent account IDs

   Valid accounts are verified against expected values and deleted after the test.
   """
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("test1", "test1", "test1@test.com", "test1", "test1", "english", status.HTTP_200_OK),   # positive test 
      ("test2", "test2", "test2@test.com", "test2", "test2", "english", status.HTTP_200_OK),   # positive test
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND),   # negative test 
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND)    # negative test -- different int generated
   ])
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
         # Create account, validate status code, and get the response data
         account = self.create_account(client, account_data, status.HTTP_201_CREATED)
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
      
      # Validate account data
      account_data = get_account_response.json()
      self.validate_account(account_data, f_name, l_name, email, username, primary_lang)
      
      # Cleanup test accounts
      self.delete_account(client, account["id"])
      
      
   """
   Tests retrieval of all accounts and validates presence of test entries.

   - Creates multiple test accounts
   - Expects 200 response from the get-all endpoint
   - Verifies all test accounts are returned with correct values
   - Cleans up all created test accounts after verification
   """
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
         # Create account, validate status code, and get the response data
         self.create_account(client, account, status.HTTP_201_CREATED)

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
         self.delete_account(client, account["id"])
         
   
   """
   Tests account deletion with valid and invalid account IDs.

   - Expects 204 when deleting an existing account
   - Expects 404 when account ID is not found

   Valid accounts are created before deletion and verified.
   """
   @pytest.mark.parametrize("f_name, l_name, email, username, password, primary_lang, status_code", [
      ("test1", "test1", "test1@test.com", "test1", "test1", "english", status.HTTP_204_NO_CONTENT),
      ("test2", "test2", "test2@test.com", "test2", "test2", "english", status.HTTP_204_NO_CONTENT),
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND),
      (None, None, None, None, None, None, status.HTTP_404_NOT_FOUND)
   ]) 
   def test_delete_account_route(self, client, f_name, l_name, email, username, password, primary_lang, status_code):
      if status_code == status.HTTP_204_NO_CONTENT:
         test_account = {
            "f_name": f_name,
            "l_name": l_name,
            "email": email,
            "username": username,
            "password": password,
            "primary_lang": primary_lang
         }
         # Create account, validate status code, and get the response data
         account = self.create_account(client, test_account, status.HTTP_201_CREATED)
         self.validate_account(account, f_name, l_name, email, username, primary_lang)
      else:
         # For negative test cases, test with random 
         random_num = random.randint(-100000, -1)
         account = {"id": random_num}
         
      # Test delete account route using account id 
      response = client.delete(f"{DELETE_ACCOUNT_URL}{account['id']}")
      assert response.status_code == status_code
      
   
   # <------------------>
   #   Helper functions
   # <------------------>
   """
   Helper function to create an account and validate the response.

   - Sends POST request with account data
   - Asserts expected status code
   - Returns created account as a JSON dict
   """
   def create_account(self, client, account_data, status_code):
      response = client.post(CREATE_ACCOUNT_URL, json=account_data)
      assert response.status_code == status_code
      return response.json()
   
   
   """
   Helper function to verify the structure and content of an account object.

   - Asserts presence of required keys
   - Asserts field values match expected input
   """
   def validate_account(self, account, f_name, l_name, email, username, primary_lang):
      assert "id" in account
      assert account["f_name"] == f_name
      assert account["l_name"] == l_name
      assert account["email"] == email
      assert account["username"] == username
      assert account["primary_lang"] == primary_lang
      

   """
   Helper function to delete an account by ID.

   - Asserts 204 response on successful deletion
   - Asserts empty response body
   """
   def delete_account(self, client, account_id):
      response = client.delete(f"{DELETE_ACCOUNT_URL}{account_id}")
      assert response.status_code == status.HTTP_204_NO_CONTENT
      assert response.text == ""
      