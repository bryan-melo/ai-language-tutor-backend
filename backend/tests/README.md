# Tests Directory

This directory contains all automated tests for the **AI-Powered Language Tutor** backend repository.

---

## Table of Contents

- [Overview](#overview)
- [Tools & Stack](#tools--stack)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Reporting](#reporting)
- [Notes](#notes)
- [References](#references)

---

## Overview

The tests validate the correctness, reliability, and robustness of backend components, including database connections, schemas, API routes, and data models.  

I use **Pytest** for automated unit and integration tests, and **Postman** for exploratory and manual API testing.

---

## Tools & Stack

- **Pytest** — main Python testing framework.
- **SQLModel & SQLAlchemy** — for setting up temporary databases.
- **Pydantic** — for schema and model validation.
- **Postman** — for manual API endpoint checks.
- **GitHub Actions** — for running automated tests on pull requests and deployments.

---

## Test Structure