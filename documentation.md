# Project Documentation - FastAPI CRUD Todo
**Course:** II.3525 - Tests & Tests Automation  
**Student:** Skyloxs  
**Date:** May 2026

---

## 1. Project Choice

For this project, I chose **FastAPI-CRUD-Todo**, a small Todo API built with FastAPI, SQLAlchemy and SQLite.

I chose it because it is simple enough to understand, but still has enough features to test properly: create, read, update, delete, filter, count, validation errors, and a small frontend.

I did not try to make a big production project. The goal was to show that I can build a complete test strategy on a small application.

---

## 2. Application Summary

The application has these main endpoints:

| Method | Endpoint | What it does |
|---|---|---|
| GET | `/` | Opens the HTML frontend |
| GET | `/api` | Simple health check |
| POST | `/todos/` | Creates a todo |
| GET | `/todos/` | Lists todos |
| GET | `/todos/count` | Counts todos |
| GET | `/todos/{id}` | Reads one todo |
| PUT | `/todos/{id}` | Updates one todo |
| DELETE | `/todos/{id}` | Deletes one todo |

A todo has:
- `id`
- `title`
- `description`
- `status`

The possible statuses are `pending`, `in_progress`, and `done`.

---

## 3. Testing Strategy

I followed the project instructions step by step:

1. I wrote a manual test plan first.
2. I automated the API tests with `pytest`.
3. I added BDD scenarios with `pytest-bdd`.
4. I used TDD for 3 small features.
5. I added one UI test with Playwright.
6. I configured GitHub Actions to run the tests automatically.

I also tried to make the test names easier to understand. For example, instead of only technical names, I used names like `test_user_can_create_todo_with_only_a_title`.

---

## 4. Tools Used

| Tool | Why I used it |
|---|---|
| `pytest` | Main test framework |
| `pytest-cov` | Code coverage |
| `pytest-bdd` | Gherkin / Given-When-Then scenarios |
| `FastAPI TestClient` | API tests without manually starting the server |
| `Playwright` | UI test in a real browser |
| `GitHub Actions` | CI/CD pipeline |

Test files are stored in the `tests/` folder. The most important files are:

```text
tests/conftest.py        shared test setup
tests/test_create.py     create tests
tests/test_read.py       read/list tests
tests/test_update.py     update tests
tests/test_delete.py     delete tests
tests/test_bug_fixes.py  checks for bugs I fixed
tests/test_bdd.py        BDD step definitions
tests/test_tdd.py        TDD feature tests
tests/test_ui.py         frontend test with Playwright
```

---

## 5. What I Improved

During the project, I found and fixed several issues:

| ID | Problem | Status |
|---|---|---|
| DEFECT-001 | Creating a todo returned `200` instead of `201` | Fixed |
| DEFECT-002 | Empty title was accepted when creating a todo | Fixed |
| DEFECT-003 | Invalid status values like `123` were accepted | Fixed |
| DEFECT-004 | Empty title could be accepted when updating a todo | Fixed |

These bugs are now covered by automated tests, so if they come back later, pytest should detect them.

---

## 6. TDD Work

I used TDD for 3 features:

1. **Empty title validation**  
   I first wrote a failing test for `title: ""`, then added `min_length=1`.

2. **Filter by status**  
   I first wrote a test for `/todos/?status=pending`, then implemented the filter.

3. **Count endpoint**  
   I first wrote a test for `/todos/count`, then added the route.

I also learned that route order matters in FastAPI, because `/todos/count` must be declared before `/todos/{id}`.

---

## 7. BDD Work

I wrote Gherkin scenarios in `tests/features/todo.feature`.

The scenarios cover:
- creating a todo,
- refusing an empty title,
- reading all todos,
- deleting a todo.

I think BDD is useful here because the scenarios are easier to read than normal Python tests.

---

## 8. UI Test

I added one UI test with Playwright.

The test does a realistic user flow:

1. Open the frontend.
2. Create a todo from the form.
3. Check that the todo appears.
4. Mark it as done.
5. Delete it.
6. Check that it disappears.

This is enough for this student project because the frontend is small.

---

## 9. CI/CD

The CI/CD pipeline is in `.github/workflows/ci.yml`.

It runs on:
- push,
- pull request,
- scheduled nightly run,
- manual trigger.

The pipeline:
1. installs Python,
2. installs dependencies,
3. installs Playwright Chromium,
4. runs API tests with coverage,
5. runs UI tests,
6. uploads test and coverage reports.

I kept only GitHub Actions to avoid having two duplicated CI configurations.

---

## 10. Results

Latest local result:

```text
31 passed
```

Coverage measured only on application code:

| File | Coverage |
|---|---:|
| `main.py` | 100% |
| `routers/todo.py` | 98% |
| `models/models.py` | 100% |
| `schemas/schemas.py` | 100% |
| `database/database.py` | 67% |
| **Total** | **95%** |

This is above the 70% requested in the instructions.

---

## 11. What I Learned

The main things I learned are:

- tests are easier to maintain when the database is reset between tests,
- coverage should be measured on application code, not on test files,
- known bugs can become regression tests after being fixed,
- UI tests are useful but should stay simple when the frontend is small,
- documentation should match the real behavior of the app.
