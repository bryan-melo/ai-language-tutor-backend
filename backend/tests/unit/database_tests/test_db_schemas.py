import pytest
from pydantic import ValidationError
from app.database.schemas import *


class TestDatabaseSchemas:
   # Test Account schema for valid instance
   def test_account_schema_valid(self):
      account = Account(
         f_name="Bryan",
         l_name="Melo",
         email="bryan@test.com",
         username="bryan123",
         password="1234",
         primary_lang="en"
      )
      
      assert account.f_name == "Bryan"
      assert account.email == "bryan@test.com" 
      
   
   # Test Account schema for invalid instance
   def test_account_schema_missing_required(self):
      with pytest.raises(ValidationError):
         Account.model_validate({
            "f_name": "Bryan",
            "l_name": "Melo",
            "username": "bryan123",
            "password": "1234",
            "primary_lang": "en"
         })
      
      