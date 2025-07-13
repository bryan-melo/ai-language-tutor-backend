import pytest
import re

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)
email_pattern = r"^[^@]+@[^@]+\.[^@]+$"


# Function to test get-all-accounts endpoint
def test_get_all_accounts():
   url = "/account/get-all-accounts"
   response = client.get(url)
      
   # Verify status code
   assert response.status_code == 200
   
   # Verify response structure in accordance with AccountRead pydantic response model
   data = response.json()
   for account in data:
      assert "id" in account
      assert "f_name" in account
      assert "l_name" in account
      assert "email" in account # re.match(email_pattern, account["email"])
      assert "username" in account
      assert "primary_lang" in account
      
   
