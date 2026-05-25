"""
test_read.py — Tests for GET /todos/ and GET /todos/{id} endpoints.

Manual test cases covered:
  - TC-006 : Read all Todos (non-empty database)
  - TC-007 : Read all Todos (empty database)
  - TC-008 : Read Todos with pagination (skip & limit)
  - TC-009 : Read an existing Todo by ID
  - TC-010 : Read a Todo with a non-existent ID
  - TC-011 : Read a Todo with an invalid (non-integer) ID
"""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def create_todo(client, title="Test Todo", description=None, status="pending"):
    """Utility to quickly create a todo and return the response JSON."""
    payload = {"title": title}
    if description:
        payload["description"] = description
    if status != "pending":
        payload["status"] = status
    resp = client.post("/todos/", json=payload)
    assert resp.status_code == 200
    return resp.json()


# ---------------------------------------------------------------------------
# TC-006 to TC-008 — Read all
# ---------------------------------------------------------------------------

def test_read_all_todos_non_empty(client):
    """TC-006 — GET /todos/ returns a list when at least one Todo exists."""
    create_todo(client, title="Todo A")
    response = client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    for item in data:
        assert "id" in item
        assert "title" in item
        assert "status" in item


def test_read_all_todos_empty_database(client):
    """TC-007 — GET /todos/ returns an empty list when the database is empty."""
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []


def test_read_todos_with_pagination(client):
    """TC-008 — GET /todos/?skip=1&limit=2 returns exactly 2 items starting from index 1."""
    create_todo(client, title="Todo 1")
    create_todo(client, title="Todo 2")
    create_todo(client, title="Todo 3")

    response = client.get("/todos/?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Todo 2"
    assert data[1]["title"] == "Todo 3"


# ---------------------------------------------------------------------------
# TC-009 to TC-011 — Read single
# ---------------------------------------------------------------------------

def test_read_single_todo_existing(client):
    """TC-009 — GET /todos/{id} returns the correct Todo for a valid existing ID."""
    created = create_todo(client, title="Single Todo", description="Test desc")
    todo_id = created["id"]

    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Single Todo"
    assert data["description"] == "Test desc"


def test_read_single_todo_not_found(client):
    """TC-010 — GET /todos/9999 returns 404 when the ID does not exist."""
    response = client.get("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_read_single_todo_invalid_id(client):
    """TC-011 — GET /todos/abc returns 422 for a non-integer path parameter."""
    response = client.get("/todos/abc")
    assert response.status_code == 422
