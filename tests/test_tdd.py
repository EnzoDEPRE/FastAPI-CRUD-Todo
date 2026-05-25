"""
test_tdd.py — TDD implementation for 3 new features.

For each feature we follow the Red -> Green -> Refactor cycle:
  RED    : write a failing test first
  GREEN  : write the minimum code to make it pass
  REFACTOR: clean up without breaking the test

Feature 1 : Title min_length validation (fixes DEFECT-002)
Feature 2 : Filter todos by status (GET /todos/?status=pending)
Feature 3 : Count todos endpoint (GET /todos/count)
"""

# ===========================================================================
# FEATURE 1 — Title must have at least 1 character (min_length validation)
# ===========================================================================
# CYCLE: RED -> GREEN -> REFACTOR (completed)
# RED:      test failed  — API accepted empty title, returned 200
# GREEN:    added Field(..., min_length=1) in schemas.py → test passed
# REFACTOR: added description="Title must not be empty" for clarity

def test_tdd_f1_red_empty_title_rejected(client):
    """
    GREEN ✅ — Empty title is now correctly rejected with 422.
    """
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


# ===========================================================================
# FEATURE 2 — Filter todos by status (GET /todos/?status=pending)
# ===========================================================================
# CYCLE: RED -> GREEN -> REFACTOR (completed)
# RED:      assert 2 == 1 — ?status param was ignored, all todos returned
# GREEN:    added Optional[str] status param + SQLAlchemy filter in router
# REFACTOR: if status is not None (more precise) + docstring added

def test_tdd_f2_red_filter_by_status(client):
    """
    RED — GET /todos/?status=pending should return only pending todos.
    Fix: add optional `status` query parameter in routers/todo.py
    """
    # Create one pending and one done todo
    client.post("/todos/", json={"title": "Pending todo", "status": "pending"})
    client.post("/todos/", json={"title": "Done todo",    "status": "done"})

    response = client.get("/todos/?status=pending")
    assert response.status_code == 200
    data = response.json()
    # Only pending todos should be returned
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert data[0]["title"] == "Pending todo"


# ===========================================================================
# FEATURE 3 — Count todos endpoint (GET /todos/count)
# ===========================================================================
# RED: this test currently FAILS because the endpoint doesn't exist yet

def test_tdd_f3_red_count_todos(client):
    """
    RED — GET /todos/count should return the total number of todos.
    Fix: add a new /count endpoint in routers/todo.py
    """
    client.post("/todos/", json={"title": "Todo 1"})
    client.post("/todos/", json={"title": "Todo 2"})
    client.post("/todos/", json={"title": "Todo 3"})

    response = client.get("/todos/count")
    assert response.status_code == 200
    assert response.json() == {"count": 3}
