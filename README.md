# QA PostgreSQL Database Automation Suite

[![Database Test Suite](https://github.com/Bunchuu/QA_PostgreSQL_v2/actions/workflows/database_tests.yml/badge.svg)](https://github.com/Bunchuu/QA_PostgreSQL_v2/actions/workflows/database_tests.yml)
![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-16--alpine-blue.svg)
![Pytest](https://img.shields.io/badge/pytest-ready-brightgreen.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)

Automated testing framework verifying PostgreSQL data integrity, relations, and transactions using Python, pytest, and psycopg2.

## Test Scope

* **Database Engine:** Version verification via `SELECT version()`.
* **Aggregation & Filtering:** Count validation via `COUNT(*)` with `WHERE` conditions.
* **M:N Relations:** Multi-table `JOIN` queries across movies and genres.
* **Transaction Isolation:** Parameterized `INSERT` operations with automatic fixture rollback (`conn.rollback()`).
* **Analytical Queries:** Grouping and aggregations with `GROUP BY` and collection checks (`all()`).
* **Lifecycle & Updates:** `UPDATE` execution with `cursor.rowcount` and numeric casting validation.
* **Negative Scenarios:** Engine-level constraint violation tests (`errors.ForeignKeyViolation`, `errors.UniqueViolation`).

## Repository Structure

```text
QA_PostgreSQL_v2/
├── .github/workflows/database_tests.yml
├── .gitignore
├── docker-compose.yml
├── conftest.py
├── pytest.ini
├── requirements.txt
├── sql/init_db.sql
├── test_database.py
└── README.md
```

## Local Setup

### 1. Start the PostgreSQL container:
```bash
docker compose up -d
```

### 2. Run Tests:
```bash
pytest
```