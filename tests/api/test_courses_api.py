import pytest

# Local file
from backend.main import app 


from fastapi.testclient import TestClient

# API URL constant
CREATE_COURSE_URL = "/courses/create/create-course"
GET_ALL_COURSES_URL = "/courses/get-all-courses"
GET_COURSE_URL = "/courses/get-course/"
DELETE_COURSE = "/courses/delete/delete-course/"


@pytest.fixture
def client():
   with TestClient(app) as c:
      yield c
      
   
class TestCourseAPI():
   # <---------------------------->
   #   Course API Endpoint Tests
   # <---------------------------->
   def test_create_course_route(self):
      pass