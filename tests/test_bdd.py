import pytest
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("features/todo.feature")


@pytest.fixture
def context():
    return {}


@given("the database is empty")
def database_is_empty():
    # The autouse clean_database fixture in conftest.py resets the database
    # before every scenario. This step keeps the scenario readable.
    return None


@given(parsers.parse('I have created a todo with title "{title}"'))
def i_have_created_todo(client, context, title):
    response = client.post("/todos/", json={"title": title})
    assert response.status_code == 201
    context["last_created_id"] = response.json()["id"]


@when(parsers.parse('I create a todo with title "{title}" and status "{status}"'))
def create_todo_with_fields(client, context, title, status):
    context["response"] = client.post("/todos/", json={"title": title, "status": status})


@when("I create a todo with an empty title")
def create_todo_empty_title(client, context):
    context["response"] = client.post("/todos/", json={"title": ""})


@when("I request the list of all todos")
def request_all_todos(client, context):
    context["response"] = client.get("/todos/")


@when("I delete the todo")
def delete_todo(client, context):
    context["response"] = client.delete(f"/todos/{context['last_created_id']}")


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
    response = client.get(f"/todos/{context['last_created_id']}")
    assert response.status_code == 404
