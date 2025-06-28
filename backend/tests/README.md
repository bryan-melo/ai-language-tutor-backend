# Tests Directory

This directory contains all automated tests for the AI-Powered Language Tutor backend repository.  

## Testing Overview

We use a combination of **Pytest** for unit and integration tests and **Postman** for exploratory API testing.  

### Purpose

- **Unit tests:** Verify individual functions and components in isolation (e.g., database connections, schemas, Pydantic models).
- **Integration tests:** Validate that database interactions and service layers work together as expected.
- **API tests:** Confirm application endpoints return expected responses and handle errors properly.

---

## Tools & Stack

- **Pytest** — main framework for all automated Python tests.
- **SQLModel & SQLAlchemy** — used to set up in-memory databases for tests.
- **Pydantic** — validates data models and schemas.
- **Postman** — used for manual and exploratory endpoint testing.
- **GitHub Actions** — for continuous integration and running tests on pull requests or before deployments.

---

## Structure