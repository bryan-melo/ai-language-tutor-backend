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
            # Missing email field
            "username": "bryan123",
            "password": "1234",
            "primary_lang": "en"
         })
         
         
   def test_course_schema_valid(self):
      course = Course(
         title="Testing Course",
         author="Bryan",
         description="This is a test",
         num_of_lessons=100,
         category="Testing",
         difficulty="Expert"
      )
      
      assert course.author == "Bryan"
      assert course.num_of_lessons == 100
      
   
   def test_course_schema_missing_required(self):
      with pytest.raises(ValidationError):
         Course.model_validate({
            "title": "Testing Course",
            "author": "Bryan",
            # Missing description field
            "num_of_lessons": 100,
            "category": "Testing",
            "difficulty": "Expert"
         })
      
      