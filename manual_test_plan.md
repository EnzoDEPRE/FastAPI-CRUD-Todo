# Manual Test Plan - FastAPI CRUD Todo
**Course:** II.3525 - Tests & Tests Automation  
**Student:** Skyloxs  
**Date:** May 2026

---

## 1. What I Am Testing

This project is a small Todo application with:
- a FastAPI backend,
- a SQLite database,
- a simple HTML frontend.

The goal of this manual test plan is to check the main user actions before and after automating them.

I am testing:
- the API health check,
- todo creation,
- todo reading and listing,
- pagination,
- status filtering,
- counting todos,
- updating todos,
- deleting todos,
- basic frontend usage,
- validation errors.

I am not testing authentication, security, performance or deployment, because the application does not really include those parts.

---

## 2. Test Objective

The objective is simple: I want to make sure that a user can manage todos normally, and that the API reacts correctly when the input is wrong.

For me, the application is acceptable if:
- normal CRUD actions work,
- wrong data returns `422`,
- unknown todos return `404`,
- creating a todo returns `201`,
- the frontend can create, update and delete a todo,
- automated tests cover at least 70% of these manual cases.

---

## 3. Test Environment

| Item | Value |
|---|---|
| OS | Windows |
| Python | 3.13 locally and in GitHub Actions |
| Backend | FastAPI / Uvicorn |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Manual tools | Browser and Swagger UI |
| Automated tools | pytest, pytest-bdd, pytest-cov, Playwright |

To run the project manually:

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Useful URLs:
- Frontend: `http://127.0.0.1:8000/`
- API health: `http://127.0.0.1:8000/api`
- Swagger docs: `http://127.0.0.1:8000/docs`

---

## 4. Manual Test Cases

I kept the cases in a table because it is easier to read and to compare with the automated tests.

| ID | Priority | Description | Preconditions | Steps | Expected Result |
|---|---|---|---|---|---|
| TC-001 | Low | Open the frontend | App is running | 1. Open `/` in a browser | Page loads with the Todo interface |
| TC-002 | Low | Check the API health route | App is running | 1. Send `GET /api` | HTTP `200` with the welcome message |
| TC-003 | High | Create a todo with all fields | App is running | 1. Send `POST /todos/` with title, description and status | HTTP `201`, response contains the created todo |
| TC-004 | High | Create a todo with only a title | App is running | 1. Send `POST /todos/` with only `title` | HTTP `201`, default status is `pending` |
| TC-005 | High | Reject a missing title | App is running | 1. Send `POST /todos/` without `title` | HTTP `422` |
| TC-006 | High | Reject an empty title on create | App is running | 1. Send `POST /todos/` with `title: ""` | HTTP `422` |
| TC-007 | High | Reject an invalid status on create | App is running | 1. Send `POST /todos/` with `status: "invalid"` | HTTP `422` |
| TC-008 | Medium | Read an empty todo list | Database is empty | 1. Send `GET /todos/` | HTTP `200`, response is `[]` |
| TC-009 | High | Read a non-empty todo list | At least one todo exists | 1. Send `GET /todos/` | HTTP `200`, response contains todos |
| TC-010 | Medium | Test pagination | At least 3 todos exist | 1. Send `GET /todos/?skip=1&limit=2` | HTTP `200`, response contains 2 todos |
| TC-011 | Medium | Filter todos by status | Todos with different statuses exist | 1. Send `GET /todos/?status=pending` | Only pending todos are returned |
| TC-012 | Medium | Count all todos | Some todos exist | 1. Send `GET /todos/count` | Response contains the current todo count |
| TC-013 | Medium | Count todos by status | Todos with different statuses exist | 1. Send `GET /todos/count?status=done` | Count matches done todos |
| TC-014 | High | Read one existing todo | A todo ID is known | 1. Send `GET /todos/{id}` | HTTP `200`, response has the correct ID |
| TC-015 | High | Try to read an unknown todo | ID `9999` does not exist | 1. Send `GET /todos/9999` | HTTP `404` |
| TC-016 | Medium | Reject an invalid ID type | App is running | 1. Send `GET /todos/abc` | HTTP `422` |
| TC-017 | High | Update all fields | A todo exists | 1. Send `PUT /todos/{id}` with title, description and status | HTTP `200`, fields are updated |
| TC-018 | High | Update only status | A todo exists | 1. Send `PUT /todos/{id}` with `{"status": "done"}` | Status changes, other fields stay the same |
| TC-019 | High | Reject empty title on update | A todo exists | 1. Send `PUT /todos/{id}` with `{"title": ""}` | HTTP `422` |
| TC-020 | High | Reject invalid status on update | A todo exists | 1. Send `PUT /todos/{id}` with `{"status": "wrong"}` | HTTP `422` |
| TC-021 | High | Try to update an unknown todo | ID `9999` does not exist | 1. Send `PUT /todos/9999` | HTTP `404` |
| TC-022 | High | Delete an existing todo | A todo exists | 1. Send `DELETE /todos/{id}` | HTTP `200`, todo is deleted |
| TC-023 | High | Check that a deleted todo is gone | A todo was deleted | 1. Send `GET /todos/{deleted_id}` | HTTP `404` |
| TC-024 | High | Try to delete an unknown todo | ID `9999` does not exist | 1. Send `DELETE /todos/9999` | HTTP `404` |
| TC-025 | High | Test the frontend flow | App is running in browser | 1. Create a todo from the page. 2. Mark it done. 3. Delete it. | Todo appears, changes status, then disappears |

---

## 5. Link With Automated Tests

| Manual cases | Automated tests |
|---|---|
| TC-001, TC-002 | `tests/test_root.py` |
| TC-003 to TC-007 | `tests/test_create.py`, `tests/test_bug_fixes.py` |
| TC-008 to TC-016 | `tests/test_read.py`, `tests/test_tdd.py` |
| TC-017 to TC-021 | `tests/test_update.py`, `tests/test_bug_fixes.py` |
| TC-022 to TC-024 | `tests/test_delete.py` |
| TC-025 | `tests/test_ui.py` |
| BDD scenarios | `tests/features/todo.feature`, `tests/test_bdd.py` |

All 25 manual cases are represented in the automated tests.

---

## 6. Small Summary

| Priority | Number of cases |
|---|---:|
| High | 18 |
| Medium | 5 |
| Low | 2 |
| **Total** | **25** |

The high priority cases are mostly about CRUD actions and validation, because those are the parts that can break the app the most.
