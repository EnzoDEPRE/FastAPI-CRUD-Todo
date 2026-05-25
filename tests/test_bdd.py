"""
test_bdd.py — BDD implementation using pytest-bdd.

Each step here implements the Gherkin scenarios defined in:
  tests/features/todo.feature

Syntax: Given / When / Then maps to the natural language in the .feature file.
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers

# Load all scenarios from the feature file
scenarios("features/todo.feature")


# ── Shared context ───────────────────────────────────────────────────────────

@pytest.fixture
def context():
    """Shared dictionary to pass data between steps."""
    return {}


# ── Given steps ─────────────────────────────────────────────────────────────

@given("the database is empty")
def database_is_empty():
    """Nothing to do — conftest.py cleans the DB before each test."""
    pass


@given(parsers.parse('I have created a todo with title "{title}"'))
def i_have_created_todo(client, context, title):
    """Pre-condition: create a todo and store its ID in context."""
    response = client.post("/todos/", json={"title": title})
    assert response.status_code == 200
    context["last_created_id"] = response.json()["id"]


# ── When steps ──────────────────────────────────────────────────────────────

@when(parsers.parse('I create a todo with title "{title}" and status "{status}"'))
def create_todo_with_fields(client, context, title, status):
    response = client.post("/todos/", json={"title": title, "status": status})
    context["response"] = response


@when("I create a todo with an empty title")
def create_todo_empty_title(client, context):
    response = client.post("/todos/", json={"title": ""})
    context["response"] = response


@when("I request the list of all todos")
def request_all_todos(client, context):
    response = client.get("/todos/")
    context["response"] = response


@when("I delete the todo")
def delete_todo(client, context):
    todo_id = context["last_created_id"]
    response = client.delete(f"/todos/{todo_id}")
    context["response"] = response


# ── Then steps ──────────────────────────────────────────────────────────────

@then(parsers.parse("the response status code should be {status_code:d}"))
def check_status_code(context, status_code):
    assert context["response"].status_code == status_code


@then(parsers.parse('the todo title should be "{title}"'))
def check_todo_title(context, title):
    assert context["response"].json()["title"] == title


@then(parsers.parse('the todo status should be "{status}"'))
def check_todo_status(context, status):
    assert context["response"].json()["status"] == status


@then(parsers.parse("the list should contain {count:d} todos"))
def check_list_count(context, count):
    assert len(context["response"].json()) == count


@then("the todo should no longer exist")
def todo_should_not_exist(client, context):
    todo_id = context["last_created_id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404
