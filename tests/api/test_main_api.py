from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_read_root():
   response = client.get("/")
   assert response.status_code == 200
   assert response.json() == {
        "message": "Welcome to the AI Language Tutor API",
        "version": "1.0",
        "routes": {
            "courses": {
                "Get course": "/courses/get-course/{course_id}",
                "Get all courses": "/courses/get-all-courses",
            },
            "lessons": {
                "Get lesson": "/lessons/get-lesson/{lesson_id}",
                "Get all lessons": "/lessons/get-all-lessons",
            }
        }
    }