import pytest
from pydantic import ValidationError
from backend.app.database.schemas import *


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
      
   
   # Test Account schema for invalid instance -- missing field
   def test_account_schema_missing_required(self):
      with pytest.raises(ValidationError):
         Account.model_validate({
            "f_name": "Bryan",
            "l_name": "Melo",
            # Missing 'email' field
            "username": "bryan123",
            "password": "1234",
            "primary_lang": "en"
         })
         
   
   # Test Course schema for valid instance
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
      
   
   # Test Course schema for invalid instance -- missing field
   def test_course_schema_missing_required(self):
      with pytest.raises(ValidationError):
         Course.model_validate({
            "title": "Testing Course",
            "author": "Bryan",
            # Missing 'description' field
            "num_of_lessons": 100,
            "category": "Testing",
            "difficulty": "Expert"
         })
         
   
   # Test Course schema for invalid instance -- atribute error
   def test_course_schema_incorrect_type(self):
      with pytest.raises(ValidationError):
         Course.model_validate({
            "title": "Test Course",
            "author": "Bryan",
            "description": "Testing Course",
            "num_of_lessons": "one hundred",   # Incorrect data type
            "category": 100,
            "difficulty": "Expert"
         })


   # Test Lesson schema for valid instance
   def test_lesson_schema_valid(self):
      lesson = Lesson(
         title="Testing Lesson",
         lesson_num=2,
         material=["Test 1", "Test 2", "Test 3"],
         parent_course=1
      )
      
      assert lesson.title == "Testing Lesson"
      assert lesson.parent_course == 1
   
   
   # Test Lesson schema for invalid instance -- missing field
   def test_lesson_schema_required(self):
      with pytest.raises(ValidationError):
         Lesson.model_validate({
            "title": "Testing Lesson 2",
            "lesson_num": 3,
            # Missing 'material' field
            "parent_course": 2
         })
         
   
   # Test Lesson schema for invalid instance -- attribute error
   def test_lesson_schema_incorrect_type(self):
      with pytest.raises(ValidationError):
         Lesson.model_validate({
            "title": "Testing Lesson 3",
            "lesson_num": "three",   # Incorrect data type
            "material": ["Test 1", "Test 2", "Test 3"],
            "parent_course": 2
         })
   