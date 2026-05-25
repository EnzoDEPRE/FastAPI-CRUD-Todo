# Manual Test Plan — FastAPI CRUD Todo
**Project:** FastAPI-CRUD-Todo  
**Course:** II.3525 – Tests & Tests Automation  
**Author:** Skyloxs  
**Date:** 2026-05-18  
**Version:** 1.0

---

## 1. Application Description & Testing Scope

### Description
FastAPI-CRUD-Todo is a RESTful API built with Python and FastAPI. It allows users to manage a list of Todo items stored in a SQLite database. The application exposes endpoints to create, read, update and delete Todo items. It is documented automatically via Swagger UI at `/docs`.

### Technology Stack
| Component | Technology |
|---|---|
| Language | Python 3.7+ |
| Framework | FastAPI |
| Database | SQLite (via SQLAlchemy ORM) |
| Validation | Pydantic |
| Server | Uvicorn |

### Testing Scope
The following API endpoints are in scope:

| Method | Endpoint | Feature |
|---|---|---|
| GET | `/` | Root / Health check |
| POST | `/todos/` | Create a new Todo |
| GET | `/todos/` | Read all Todos (with pagination) |
| GET | `/todos/{id}` | Read a single Todo by ID |
| PUT | `/todos/{id}` | Update a Todo by ID |
| DELETE | `/todos/{id}` | Delete a Todo by ID |

**Out of scope:** Authentication, authorization, frontend UI (none exists), performance/load testing.

---

## 2. Testing Objectives & Acceptance Criteria

### Objectives
- Verify that each CRUD endpoint behaves correctly under normal (happy path) conditions.
- Verify that the API handles erroneous inputs and edge cases gracefully.
- Verify that HTTP status codes and response bodies conform to the expected contract.
- Verify that database state is correctly modified by each operation.

### Acceptance Criteria
- All happy path test cases must **PASS**.
- All error/edge case endpoints must return the correct HTTP status code and a meaningful error message.
- No endpoint should return a 500 Internal Server Error for any documented input.
- The `id` field returned in responses must be a positive integer auto-incremented by the database.
- Optional fields (`description`, `status`) must use their default values when not provided.

---

## 3. Features to be Tested

1. **Root endpoint** — Health check, verifies the application is running.
2. **Create Todo** — Creates a new item with `title`, optional `description`, and optional `status` (default: `"pending"`).
3. **Read all Todos** — Returns a paginated list of all Todo items (`skip` and `limit` query parameters).
4. **Read single Todo** — Returns a single Todo by its integer `id`.
5. **Update Todo** — Partially or fully updates an existing Todo's `title`, `description`, and/or `status`.
6. **Delete Todo** — Removes a Todo from the database by its `id`.
7. **Error handling (404)** — Correct error returned when a non-existent ID is requested.
8. **Input validation** — Correct error returned when required fields are missing or malformed.

---

## 4. Test Environment

| Item | Value |
|---|---|
| OS | Windows 10/11 or Linux |
| Python version | 3.10+ |
| Server | `uvicorn main:app --reload` |
| Base URL | `http://127.0.0.1:8000` |
| API Doc URL | `http://127.0.0.1:8000/docs` |
| Test Tool | Swagger UI (`/docs`) or `curl` / Postman |
| Database | SQLite — `todo.db` (auto-created on startup) |

### Setup Steps
```bash
# 1. Create and activate virtual environment
python -m venv env
source env/bin/activate       # macOS/Linux
.\env\Scripts\activate        # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload

# 4. Open http://127.0.0.1:8000/docs in your browser
```

---

## 5. Manual Test Cases

---

### Feature 1 — Root Endpoint

#### TC-001 — Health Check
| Field | Detail |
|---|---|
| **Test Case ID** | TC-001 |
| **Feature** | Root Endpoint |
| **Description** | Verify the root endpoint returns a welcome message and a 200 OK status. |
| **Preconditions** | Application is running at `http://127.0.0.1:8000` |
| **Priority** | Low |

**Steps:**
1. Send a `GET` request to `http://127.0.0.1:8000/`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: `{"message": "Welcome to the Enhanced FastAPI Todo App!"}`

---

### Feature 2 — Create Todo

#### TC-002 — Create a Todo with all fields
| Field | Detail |
|---|---|
| **Test Case ID** | TC-002 |
| **Feature** | Create Todo |
| **Description** | Create a new Todo item providing title, description, and status. |
| **Preconditions** | Application is running. Database may be empty or contain existing items. |
| **Priority** | High |

**Steps:**
1. Send a `POST` request to `/todos/` with the following JSON body:
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

**Expected Result:**
- HTTP Status: `201 Created`
- Response body contains:
  - `id`: a positive integer
  - `title`: `"Buy groceries"`
  - `description`: `"Milk, eggs, bread"`
  - `status`: `"pending"`

---

#### TC-003 — Create a Todo with title only (optional fields omitted)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-003 |
| **Feature** | Create Todo |
| **Description** | Create a Todo providing only the required `title` field. Verify defaults are applied. |
| **Preconditions** | Application is running. |
| **Priority** | High |

**Steps:**
1. Send a `POST` request to `/todos/` with body:
```json
{
  "title": "Call dentist"
}
```

**Expected Result:**
- HTTP Status: `201 Created`
- Response body:
  - `id`: a positive integer
  - `title`: `"Call dentist"`
  - `description`: `null`
  - `status`: `"pending"` (default value applied)

---

#### TC-004 — Create a Todo without required field `title`
| Field | Detail |
|---|---|
| **Test Case ID** | TC-004 |
| **Feature** | Create Todo — Input Validation |
| **Description** | Attempt to create a Todo without the required `title` field. |
| **Preconditions** | Application is running. |
| **Priority** | High |

**Steps:**
1. Send a `POST` request to `/todos/` with body:
```json
{
  "description": "No title provided"
}
```

**Expected Result:**
- HTTP Status: `422 Unprocessable Entity`
- Response body contains a validation error mentioning the missing `title` field.

---

#### TC-005 — Create a Todo with empty title string
| Field | Detail |
|---|---|
| **Test Case ID** | TC-005 |
| **Feature** | Create Todo — Input Validation |
| **Description** | Attempt to create a Todo with an empty string as title. |
| **Preconditions** | Application is running. |
| **Priority** | Medium |

**Steps:**
1. Send a `POST` request to `/todos/` with body:
```json
{
  "title": ""
}
```

**Expected Result:**
- HTTP Status: `422 Unprocessable Entity` (or `400 Bad Request`)
- Response body contains a validation error indicating the title cannot be empty.

> **Note:** The current implementation does not enforce a minimum length on `title`. This test may reveal a defect to document.

---

### Feature 3 — Read All Todos

#### TC-006 — Read all Todos (non-empty database)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-006 |
| **Feature** | Read All Todos |
| **Description** | Retrieve the full list of Todos when at least one item exists. |
| **Preconditions** | At least one Todo has been created (e.g., run TC-002 first). |
| **Priority** | High |

**Steps:**
1. Send a `GET` request to `/todos/`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: a JSON array containing at least one Todo object.
- Each object has fields: `id`, `title`, `description`, `status`.

---

#### TC-007 — Read all Todos (empty database)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-007 |
| **Feature** | Read All Todos |
| **Description** | Retrieve the list when no Todos exist in the database. |
| **Preconditions** | Database is empty (fresh start or all items deleted). |
| **Priority** | Medium |

**Steps:**
1. Ensure database is empty.
2. Send a `GET` request to `/todos/`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: `[]` (empty array)

---

#### TC-008 — Read Todos with pagination (skip & limit)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-008 |
| **Feature** | Read All Todos — Pagination |
| **Description** | Verify that `skip` and `limit` query parameters correctly paginate results. |
| **Preconditions** | At least 3 Todos exist in the database. |
| **Priority** | Medium |

**Steps:**
1. Send a `GET` request to `/todos/?skip=1&limit=2`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: a JSON array containing exactly 2 items, starting from the second Todo in the database.

---

### Feature 4 — Read Single Todo

#### TC-009 — Read an existing Todo by ID
| Field | Detail |
|---|---|
| **Test Case ID** | TC-009 |
| **Feature** | Read Single Todo |
| **Description** | Retrieve a specific Todo using its integer ID. |
| **Preconditions** | A Todo with a known ID exists (e.g., created in TC-002, ID = 1). |
| **Priority** | High |

**Steps:**
1. Send a `GET` request to `/todos/1`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: the Todo object with `id: 1` and correct field values.

---

#### TC-010 — Read a Todo with a non-existent ID
| Field | Detail |
|---|---|
| **Test Case ID** | TC-010 |
| **Feature** | Read Single Todo — Error Handling |
| **Description** | Attempt to retrieve a Todo using an ID that does not exist in the database. |
| **Preconditions** | Application is running. ID `9999` does not exist. |
| **Priority** | High |

**Steps:**
1. Send a `GET` request to `/todos/9999`.

**Expected Result:**
- HTTP Status: `404 Not Found`
- Response body: `{"detail": "Todo not found"}`

---

#### TC-011 — Read a Todo with an invalid (non-integer) ID
| Field | Detail |
|---|---|
| **Test Case ID** | TC-011 |
| **Feature** | Read Single Todo — Input Validation |
| **Description** | Attempt to retrieve a Todo using a string as the ID parameter. |
| **Preconditions** | Application is running. |
| **Priority** | Medium |

**Steps:**
1. Send a `GET` request to `/todos/abc`.

**Expected Result:**
- HTTP Status: `422 Unprocessable Entity`
- Response body contains a validation error about the invalid path parameter type.

---

### Feature 5 — Update Todo

#### TC-012 — Update all fields of an existing Todo
| Field | Detail |
|---|---|
| **Test Case ID** | TC-012 |
| **Feature** | Update Todo |
| **Description** | Fully update the title, description, and status of an existing Todo. |
| **Preconditions** | A Todo with ID 1 exists. |
| **Priority** | High |

**Steps:**
1. Send a `PUT` request to `/todos/1` with body:
```json
{
  "title": "Buy groceries — UPDATED",
  "description": "Milk, eggs, bread, butter",
  "status": "in_progress"
}
```

**Expected Result:**
- HTTP Status: `200 OK`
- Response body reflects the updated values:
  - `title`: `"Buy groceries — UPDATED"`
  - `description`: `"Milk, eggs, bread, butter"`
  - `status`: `"in_progress"`
  - `id`: unchanged (still `1`)

---

#### TC-013 — Partially update a Todo (only status)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-013 |
| **Feature** | Update Todo — Partial Update |
| **Description** | Update only the `status` field of a Todo, leaving other fields unchanged. |
| **Preconditions** | A Todo with ID 1 exists with `title: "Buy groceries"`. |
| **Priority** | High |

**Steps:**
1. Send a `PUT` request to `/todos/1` with body:
```json
{
  "status": "done"
}
```

**Expected Result:**
- HTTP Status: `200 OK`
- Response body:
  - `status`: `"done"`
  - `title`: unchanged from its previous value
  - `description`: unchanged from its previous value

---

#### TC-014 — Update a Todo with a non-existent ID
| Field | Detail |
|---|---|
| **Test Case ID** | TC-014 |
| **Feature** | Update Todo — Error Handling |
| **Description** | Attempt to update a Todo that does not exist. |
| **Preconditions** | ID `9999` does not exist in the database. |
| **Priority** | High |

**Steps:**
1. Send a `PUT` request to `/todos/9999` with body:
```json
{
  "title": "Ghost update"
}
```

**Expected Result:**
- HTTP Status: `404 Not Found`
- Response body: `{"detail": "Todo not found"}`

---

### Feature 6 — Delete Todo

#### TC-015 — Delete an existing Todo
| Field | Detail |
|---|---|
| **Test Case ID** | TC-015 |
| **Feature** | Delete Todo |
| **Description** | Delete a Todo that exists in the database. |
| **Preconditions** | A Todo with a known ID exists (e.g., ID = 1). |
| **Priority** | High |

**Steps:**
1. Send a `DELETE` request to `/todos/1`.

**Expected Result:**
- HTTP Status: `200 OK`
- Response body: `{"detail": "Todo deleted"}`

---

#### TC-016 — Verify Todo is deleted (read after delete)
| Field | Detail |
|---|---|
| **Test Case ID** | TC-016 |
| **Feature** | Delete Todo — Post-condition check |
| **Description** | After deletion, verify the Todo can no longer be retrieved. |
| **Preconditions** | TC-015 has been executed successfully (ID 1 deleted). |
| **Priority** | High |

**Steps:**
1. Send a `GET` request to `/todos/1`.

**Expected Result:**
- HTTP Status: `404 Not Found`
- Response body: `{"detail": "Todo not found"}`

---

#### TC-017 — Delete a Todo with a non-existent ID
| Field | Detail |
|---|---|
| **Test Case ID** | TC-017 |
| **Feature** | Delete Todo — Error Handling |
| **Description** | Attempt to delete a Todo using an ID that does not exist. |
| **Preconditions** | ID `9999` does not exist in the database. |
| **Priority** | High |

**Steps:**
1. Send a `DELETE` request to `/todos/9999`.

**Expected Result:**
- HTTP Status: `404 Not Found`
- Response body: `{"detail": "Todo not found"}`

---

## 6. Test Case Summary

| ID | Feature | Description | Priority | Expected Status |
|---|---|---|---|---|
| TC-001 | Root | Health check | Low | 200 |
| TC-002 | Create | All fields provided | High | 201 |
| TC-003 | Create | Title only (defaults) | High | 201 |
| TC-004 | Create | Missing required field | High | 422 |
| TC-005 | Create | Empty title string | Medium | 422 |
| TC-006 | Read All | Non-empty database | High | 200 |
| TC-007 | Read All | Empty database | Medium | 200 |
| TC-008 | Read All | Pagination (skip/limit) | Medium | 200 |
| TC-009 | Read One | Existing ID | High | 200 |
| TC-010 | Read One | Non-existent ID | High | 404 |
| TC-011 | Read One | Invalid ID type | Medium | 422 |
| TC-012 | Update | Full update | High | 200 |
| TC-013 | Update | Partial update (status only) | High | 200 |
| TC-014 | Update | Non-existent ID | High | 404 |
| TC-015 | Delete | Existing Todo | High | 200 |
| TC-016 | Delete | Read after delete | High | 404 |
| TC-017 | Delete | Non-existent ID | High | 404 |

**Total: 17 test cases** — 11 High priority, 5 Medium, 1 Low.
