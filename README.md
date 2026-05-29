# FastAPI CRUD Todo - Tests & Automation

This project is a FastAPI Todo application used for the II.3525 catch-up project on testing and test automation.

It contains:
- A REST API for Todo CRUD operations
- A small HTML frontend for demos
- Manual test plan
- Automated API tests with pytest
- BDD scenarios with pytest-bdd
- UI test with Playwright
- Coverage reports with pytest-cov
- GitHub Actions CI configuration

## Features

- Create a todo
- List todos with pagination
- Filter todos by status
- Count todos
- Read one todo
- Update a todo
- Delete a todo
- Validate title and status values

Accepted status values:
- `pending`
- `in_progress`
- `done`

## Run the App

```bash
python -m venv env
.\env\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open:
- Frontend: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/api`

## Run Tests

API, BDD and TDD tests:

```bash
pytest tests/ -v -m "not ui"
```

Coverage on application code:

```bash
pytest tests/ -v -m "not ui" --cov=main --cov=routers --cov=models --cov=schemas --cov=database --cov-report=term-missing
```

UI tests:

```bash
python -m playwright install chromium
pytest tests/ -v -m ui
```

## Project Structure

```text
database/       Database setup
models/         SQLAlchemy models
routers/        FastAPI routes
schemas/        Pydantic schemas and validation
static/         HTML frontend
tests/          Automated API, BDD, TDD and UI tests
.github/        GitHub Actions pipeline
```

## Documentation

- `manual_test_plan.md`: manual campaign and test cases
- `documentation.md`: strategy, metrics, defects and CI/CD explanation
