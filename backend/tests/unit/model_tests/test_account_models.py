import pytest
from pydantic import ValidationError
from app.models.account_models import AccountRead, LoginRequest


class TestAccountModels:
   # Test AccountRead model for valid instance
   def test_account_read_valid(self):
      data = {
         "id": 1,
         "f_name": "Bryan",
         "l_name": "Melo",
         "email": "bryan@test.com",
         "username": "Tester",
         "primary_lang": "English"
      }
      model = AccountRead(**data)
      
      assert model.id == 1
      assert model.username == "Tester"
      
      
   # Test AccountRead model for invalid instance -- missing field
   def test_account_read_missing_field(self):
      with pytest.raises(ValidationError):
         AccountRead.model_validate({
            "id": 1,
            "f_name": "Bryan",
            # Missing 'l_name' field
            "email": "bryan@test.com",
            "username": "Tester",
            "primary_lang": "English"
      })
         
   
   # Test AccountRead model for invalid instance -- mispelled field
   def test_account_read_mispelled_field(self):
      with pytest.raises(ValidationError):
         AccountRead.model_validate({
            "idd": 1,   # id mispelled
            "f_name": "Bryan",
            "l_name": "Melo",
            "email": "bryan@test.com",
            "username": "Tester",
            "primary_lang": "English"
         })
         
   
   # Test LoginRequest model for valid instance
   def test_login_request_valid(self):
      data = {
         "username": "Tester",
         "password": "1234"
      }
      login_request = LoginRequest(**data)
      
      assert login_request.username == "Tester"
      assert login_request.password == "1234"
      
      
   # Test LoginRequest model for invalid instance -- missing field
   def test_login_request_missing_field(self):
      with pytest.raises(ValidationError):
         LoginRequest.model_validate({
            "username": "Tester",
            # Missing 'password' field
         })
         
         
   # Test LoginRequest model for invalid instance -- mispelled field
   def test_login_request_mispelled_field(self):
      with pytest.raises(ValidationError):
         LoginRequest.model_validate({
            "username": "Tester",
            "passwordd": "1234",    # Password mispelled
         })
