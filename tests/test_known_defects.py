"""
test_known_defects.py — Tests that deliberately FAIL to highlight known defects.

These tests document bugs found during the manual testing campaign.
They are expected to FAIL until the defects are fixed in the source code.
Each test is marked with @pytest.mark.xfail so pytest reports them as
XFAIL (expected failure) rather than ERROR, keeping the test suite clean.

Defects documented here:
  - DEFECT-001 : POST /todos/ returns 200 instead of 201 (RFC 7231 violation)
  - DEFECT-002 : POST /todos/ accepts empty string as title (missing min_length validation)
"""

import pytest


# ---------------------------------------------------------------------------
# DEFECT-001
# ---------------------------------------------------------------------------


@pytest.mark.xfail(strict=True, reason="DEFECT-001: POST /todos/ returns 200 instead of 201 Created")
def test_create_todo_should_return_201(client):
    """
    DEFECT-001 — POST /todos/ should return HTTP 201 Created, not 200 OK.

    According to RFC 7231, a POST endpoint that creates a new resource
    should respond with 201 Created. The current implementation returns
    200 OK, which is technically incorrect.

    Status   : OPEN
    Severity : Low
    Fix      : Add `status_code=201` to the @router.post() decorator in routers/todo.py
    """
    payload = {"title": "Defect test todo"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 201  # Currently returns 200 → FAILS → XFAIL ✓


# ---------------------------------------------------------------------------
# DEFECT-002
# ---------------------------------------------------------------------------

def test_create_todo_empty_title_is_now_fixed(client):
    """
    DEFECT-002 — FIXED ✅

    Empty title string is now correctly rejected with 422.
    Fixed via TDD Feature 1: min_length=1 added to schemas.py.
    This test now serves as a regression guard.
    """
    payload = {"title": ""}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# DEFECT-003
# ---------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="DEFECT-003: Invalid status value is accepted, should return 422")
def test_create_todo_invalid_status_should_be_rejected(client):
    """
    DEFECT-003 — POST /todos/ accepts any arbitrary string as status value.

    The `status` field in TodoCreate is defined as Optional[str] with no
    constraint on allowed values. This means any string — including "123",
    "invalid", or "foobar" — is accepted and persisted in the database,
    breaking the expected state machine (pending → in_progress → done).

    Discovered during manual testing: creating a todo with status="123"
    returns 200 OK and stores the invalid value.

    Status   : OPEN
    Severity : Medium
    Fix      : Replace Optional[str] with a proper Enum in schemas/schemas.py:
                 from enum import Enum
                 class StatusEnum(str, Enum):
                     pending     = "pending"
                     in_progress = "in_progress"
                     done        = "done"
                 Then use: status: StatusEnum = StatusEnum.pending
    """
    payload = {"title": "Valid title", "status": "123"}
    response = client.post("/todos/", json=payload)
    assert response.status_code == 422  # Currently returns 200 → FAILS → XFAIL ✓


@pytest.mark.xfail(strict=True, reason="DEFECT-003: Invalid status value accepted on update too")
def test_update_todo_invalid_status_should_be_rejected(client):
    """
    DEFECT-003b — PUT /todos/{id} also accepts invalid status values.

    Same root cause as DEFECT-003 — the TodoUpdate schema has the same
    unconstrained Optional[str] on the status field.

    Status   : OPEN
    Severity : Medium
    Fix      : Same Enum fix applies to TodoUpdate schema in schemas/schemas.py
    """
    # Create a valid todo first
    create_resp = client.post("/todos/", json={"title": "Test todo"})
    assert create_resp.status_code == 200
    todo_id = create_resp.json()["id"]

    # Try to update with an invalid status
    response = client.put(f"/todos/{todo_id}", json={"status": "nimportequoi"})
    assert response.status_code == 422  # Currently returns 200 → FAILS → XFAIL ✓
