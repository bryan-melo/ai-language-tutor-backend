# API Test Plan

## Overview
This document outlines the test plan for validating API endpoints in the AI-Powered Language Tutor backend.

--- 

## Test Objectives
- Verify each endpoint works as expected with valid data.
- Ensure proper error handling with invalid or missing data.
- Check HTTP status codes and response schemas.

---

## Endpoints to Test

### /account

- **POST '/create/create-account'**
   - **Positive:** Account is successfully created when all required fields are valid.
   - **Negative:** Fails to create an account when fields are missing, email is invalid, username is duplicated, or password requirements are not met.
   - **Expected status code:**
      - 201 Created
      - 400 Bad Request
      - 409 Conflict

- **POST '/login'**
   - **Positive:** Login succeeds with correct credentials and returns a valid authentication schema.
   - **Negative:** Login fails with incorrect credentials; returns appropriate error message.
   - **Expected status code:**
      - 200 OK
      - 401 Unauthorized

- **GET '/get-all-accounts'**
   - **Positive:** Retrieves all accounts when authorized; returns correct schema.
   - **Negative:** Request denied without proper permissions.
   - **Expected status code:**
      - 200 OK
      - 403 Forbidden

- **GET '/get-account/{account_id}'**
   - **Positive:** Retrieves the specified account when authorized.
   - **Negative:** Access denied or account does not exist.
   - **Expected status code:**
      - 200 OK
      - 403 Forbidden
      - 404 Not Found

- **DELETE '/delete/delete-account/{account_id}'**
   - **Positive:** Account is successfully deleted when authorized.
   - **Negative:** Unauthorized deletion attempt or account does not exist.
   - **Expected status code:**
      - 200 OK
      - 204 No Content
      - 403 Forbidden
      - 404 Not Found

---

### /openai

- **POST '/chat'**
   - **Positive:** Chat API returns a valid, generated response from the prompt.
   - **Negative:** Request fails due to invalid or missing input; returns error.
   - **Expected status code:**
      - 200 OK
      - 400 Bad Request

---

### /courses

- **POST '/create/create-course'**
   - **Positive:** Course is successfully created and schema is validated.
   - **Negative:** Course creation fails due to invalid input or missing fields.
   - **Expected status code:**
      - 201 Created
      - 400 Bad Request

- **GET '/get-all-courses'**
   - **Positive:** Retrieves all courses with correct schema.
   - **Negative:** Courses cannot be retrieved (e.g., database error).
   - **Expected status code:**
      - 200 OK
      - 500 Internal Server Error

- **GET '/get-course/{course_id}'**
   - **Positive:** Retrieves the specified course and validates schema.
   - **Negative:** Course not found.
   - **Expected status code:**
      - 200 OK
      - 404 Not Found

- **DELETE '/delete/delete-course/{course_id}'**
   - **Positive:** Deletes the specified course successfully.
   - **Negative:** Course not found or deletion unauthorized.
   - **Expected status code:**
      - 200 OK
      - 204 No Content
      - 403 Forbidden
      - 404 Not Found

--- 

### /courses/lessons

- **POST '/create/create-lesson'**
   - **Positive:** Lesson is created, properly linked to parent course, and schema is validated.
   - **Negative:** Lesson creation fails due to missing fields or invalid parent course reference.
   - **Expected status code:**
      - 201 Created
      - 400 Bad Request

- **GET '/get-lessons-by-course/{course_id}'**
   - **Positive:** Retrieves all lessons for the given course ID with correct schema.
   - **Negative:** Lessons not found for the given course ID.
   - **Expected status code:**
      - 200 OK
      - 404 Not Found

- **GET '/get-lesson/{lesson_id}'**
   - **Positive:** Retrieves the specified lesson and validates schema.
   - **Negative:** Lesson not found.
   - **Expected status code:**
      - 200 OK
      - 404 Not Found

- **DELETE '/delete/delete-lesson/{lesson_id}'**
   - **Positive:** Deletes the specified lesson successfully.
   - **Negative:** Lesson not found or deletion unauthorized.
   - **Expected status code:**
      - 200 OK
      - 204 No Content
      - 403 Forbidden
      - 404 Not Found
      
---

## Tools

- Pytest
- httpx (for making HTTP requests)
- FastAPI TestClient (for local tests)

---

## Future Considerations

- Add performance tests.
- Add schema validation with Pydantic models.
- Extend negative cases to include SQL injection or security checks.