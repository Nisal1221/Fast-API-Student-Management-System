
# Student Management System API

[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-V2-E92063?style=flat&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/Tests-Pytest%20Passed-brightgreen?style=flat&logo=pytest&logoColor=white)]()

An asynchronous RESTful backend built with FastAPI, SQLAlchemy (Async ORM), SQLite/PostgreSQL, and JWT security for student-course enrollment workflows.

---

## Features

- **JWT Authentication & RBAC:** Secure password hashing with Passlib/Bcrypt, OAuth2 Password Bearer flow, and route protection dependencies.
- **Async Database Architecture:** Non-blocking database transactions powered by SQLAlchemy 2.0 and async drivers.
- **Many-to-Many Relationships:** Association table mapping for students and course enrollments with cascade cleanup.
- **Input Validation & Schemas:** Strict payload and response sanitization using Pydantic V2 `ConfigDict`.
- **Interactive Documentation:** Automatic OpenAPI generation via Swagger UI (`/docs`) and ReDoc (`/redoc`).
- **Containerization & Tests:** Multi-stage `Dockerfile`, `docker-compose.yml`, and asynchronous unit test coverage with `pytest` and `httpx`.

---

## Entity Relationship (ER) Design

```text
  ┌───────────────┐              ┌───────────────────┐              ┌───────────────┐
  │   STUDENTS    │              │  STUDENT_COURSES  │              │    COURSES    │
  ├───────────────┤              ├───────────────────┤              ├───────────────┤
  │ PK │ id       │1            *│ PK,FK1 │ student_id│*            1│ PK │ id       │
  │    │ email    ├─────────────►│ PK,FK2 │ course_id ◄──────────────┤    │ code     │
  │    │ names... │              │        │           │              │    │ title... │
  └───────────────┘              └───────────────────┘              └───────────────┘
Quickstart
Local Setup
Bash
# Clone repository
git clone https://github.com/Nisal1221/Fast-API-Student-Management-System
cd Fast-API-Student-Management-System

# Initialize virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Linux/macOS: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Populate demo data
python seed.py

# Run development server
uvicorn app.main:app --reload
Interactive API documentation available at http://127.0.0.1:8000/docs.

Run via Docker Compose

docker-compose up --build

Run Test Suite

python -m pytest

