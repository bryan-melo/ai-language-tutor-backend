
# Tests Directory

This directory serves as a high-level overview of tests created for the **AI-Powered Language Tutor** backend repository.

---

## Table of Contents
1. [Overview](#overview)
2. [Tools & Stack](#tools--stack) 
3. [Test File Structure](#test-file-structure)
4. [Running Tests](#running-tests)
5. [Reporting](#reporting)
6. [Notes](#notes)
7. [References](#references)

---

## Overview

The tests ensure correctness, reliability, and robustness of backend components, including:

- Database connections
- Schemas
- API routes
- Data models

I use **Pytest** for automated unit and integration tests, and **Postman** for exploratory and manual API testing.

---

## Tools & Stack

- **Pytest** — Unit and API testing framework.
- **SQLModel & SQLAlchemy** — Database interactions and test databases.
- **Pydantic** — Data validation for schemas and models.
- **Postman** — Manual and exploratory API testing.
- **GitHub Actions** — CI/CD automated checks.

---

## Test File Structure

```
tests/
├── api/           # API endpoint tests using TestClient
├── unit/          # Unit tests for database connections, schemas, models
│   └── database_tests/
│       ├── test_db_connection.py
│       ├── test_db_schemas.py
│       └── ...
├── integration/   # Planned integration tests
├── ui/            # Planned Selenium UI tests
```

**Unit tests:** Test small, isolated pieces (functions, schemas).  
**API tests:** Validate route logic and responses.  
**Integration tests (planned):** Check end-to-end workflows.  
**UI tests (planned):** Automate frontend flows like login and lesson tracking.

---

## Running Tests

```bash
# Run all tests
pytest

# Run and generate an HTML report
pytest --html=all_unit_test_report.html

# Run a single test file
pytest tests/unit/database_tests/test_db_connection.py

# Run tests in parallel (if configured)
pytest -n auto
```

---

## Reporting

- HTML reports (e.g., `all_unit_test_06262025.html`) summarize pass/fail status.
- Includes tracebacks, runtime, and detailed breakdowns.
- HTML reports are stored under 'reports/' directory.

---

## Notes

- Tests include positive, negative, and edge case scenarios.
- Database tests use an in-memory SQLite engine to avoid touching production data.
- Tests are designed to run in CI/CD pipelines (GitHub Actions).

---

## References

- Pytest: https://docs.pytest.org/en/stable/
- Postman: https://www.postman.com/
- SQLModel: https://sqlmodel.tiangolo.com/
- FastAPI: https://fastapi.tiangolo.com/

---

_Last updated: June 28, 2025._