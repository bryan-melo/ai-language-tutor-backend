# API Test Plan
This document outlines the **test plan** for validating API endpoints in the AI-Powered Language Tutor backend.

## 📄 Table of Contents

1. [Test Objectives](#test-objectives)
2. [RESTful APIs Foundational Knowledge](#restful-apis-foundational-knowledge)
   - [HTTP Methods](#http-methods)
   - [Status Codes](#status-codes)
   - [Validation](#validation)
3. [Endpoints to Test](#endpoints-to-test)
   - [Account Endpoints](#account)
   - [OpenAI Endpoints](#openai)
   - [Courses Endpoints](#courses)
   - [Lessons Endpoints](#courseslessons)
4. [Tools](#tools)
5. [Future Considerations](#future-considerations)
6. [Resources](#resources)

--- 

## Test Objectives
- Verify each endpoint works as expected with valid data. 
- Ensure proper error handling with invalid or missing data.
- Check HTTP status codes and response schemas.

---

## RESTful APIs Foundational Knowledge

### HTTP Methods
- **GET**: Retrieves data from the server
- **POST**: Creates a new resource on the server
- **PUT**: Updates an existing resource on the server
- **DELETE**: Removes a resource from the server

### Status Codes
- **2xx Success**: Indicates successful actions
- **4xx Client Error**: Signals an issue likely related to the request itself
- **5xx Server Error**: Points to problems on the server side

### Validation
- **Structure**: Verify that the response adheres to the expected format (typically JSON for RESTful APIs)
- **Content-Type**: Confirm that the Content-Type header correctly specifies the format of the response
- **Data Integrity**: Check that the data within the response matches your expectations, both in terms of values and their types

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

### courses/lessons

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

---

## Resources
- [How to Write a QA Test Plan](https://testlio.com/blog/write-qa-test-plan/)
- [pytest how-to guides](https://docs.pytest.org/en/stable/how-to/index.html)
- [HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status)
- [Send responses to HTTPX using pytest](https://pypi.org/project/pytest-httpx/)
- [HTTP modules](https://docs.python.org/3/library/http.html)
- [Produce coverage reports](https://pypi.org/project/pytest-cov/)
