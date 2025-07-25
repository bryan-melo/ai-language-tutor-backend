import pytest

from typing import Any
from fastapi import status
from fastapi.testclient import TestClient

# Local file
from backend.main import app 
from backend.app.models.course_models import CourseCreate
from backend.app.models.course_models import CourseCategories, CourseDifficulty
from .utils import validate_and_create_instance, delete_instance

# API URL constant
CREATE_COURSE_URL = "/courses/create/create-course"
GET_ALL_COURSES_URL = "/courses/get-all-courses"
GET_COURSE_URL = "/courses/get-course/"
DELETE_COURSE_URL = "/courses/delete/delete-course/"


@pytest.fixture
def client():
   with TestClient(app) as c:
      yield c
      

class TestCourseAPI():
   # <---------------------------->
   #   Course API Endpoint Tests
   # <---------------------------->
   @pytest.mark.parametrize("course_data, status_code", [
      ({"title": "test_course_1", "author": "test1", "description": "Test course", "num_of_lessons": 1, "category": "Pronunciation & Phonetics", "difficulty": "Beginner"}, status.HTTP_201_CREATED)
   ])
   def test_create_course_route(self, client: TestClient, course_data: dict[str, Any], status_code: int):
      # Validate input data using Pydantic model before sending request
      response_data = validate_and_create_instance(client, CourseCreate, course_data, status_code, CREATE_COURSE_URL)
      
      if status_code == status.HTTP_422_UNPROCESSABLE_ENTITY or not response_data:
         return
      
      # Validate fields match expected values
      self.validate_course(
         response_data,
         course_data['title'],
         course_data['author'],
         course_data['description'],
         course_data['num_of_lessons'],
         course_data['category'],
         course_data['difficulty']
      )
      
      # Clean up test courses
      delete_instance(client, response_data["id"], DELETE_COURSE_URL)
      
      
   def test_get_all_courses_route(self, client: TestClient):
      response_data = client.get(GET_ALL_COURSES_URL)
      
      assert response_data.status_code == status.HTTP_200_OK
      
      
      

   # <------------------>
   #   Helper functions
   # <------------------> 
   def validate_course(self, course: dict[str, Any], title: str, author: str, description: str, num_of_lessons: int, category: str, difficulty: str):
      assert course['id'] is not None, "Expected course.id to be populated"
      assert course["title"] == title, f"Expected title={title}, got {course['title']}"
      assert course["author"] == author, f"Expected author={author}, got {course['author']}"
      assert course["description"] == description, f"Expected description={description}. got {course['description']}"
      assert course["num_of_lessons"] == num_of_lessons, f"Expected num_of_lessons={num_of_lessons}, got {course['num_of_lessons']}"

      # Validate category
      assert CourseCategories(course["category"]), f"Invalid category value: {course['category']}"
      assert course["category"] == category, f"Expected category={category}, got {course['category']}"

      # Validate difficulty
      assert CourseDifficulty(course["difficulty"]), f"Invalid difficulty value: {course['difficulty']}"
      assert course["difficulty"] == difficulty, f"Expected difficulty={difficulty}, got {course['difficulty']}"
