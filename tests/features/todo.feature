Feature: Todo API
  As a user of the Todo API
  I want to manage my todo items
  So that I can keep track of my tasks

  # ── Scenario 1 ──────────────────────────────
  Scenario: Create a todo with all fields
    Given the database is empty
    When I create a todo with title "Buy groceries" and status "pending"
    Then the response status code should be 200
    And the todo title should be "Buy groceries"
    And the todo status should be "pending"

  # ── Scenario 2 ──────────────────────────────
  Scenario: Refuse to create a todo with an empty title
    Given the database is empty
    When I create a todo with an empty title
    Then the response status code should be 422

  # ── Scenario 3 ──────────────────────────────
  Scenario: Read all todos
    Given the database is empty
    And I have created a todo with title "Task A"
    And I have created a todo with title "Task B"
    When I request the list of all todos
    Then the response status code should be 200
    And the list should contain 2 todos

  # ── Scenario 4 ──────────────────────────────
  Scenario: Delete a todo and verify it no longer exists
    Given the database is empty
    And I have created a todo with title "To be deleted"
    When I delete the todo
    Then the response status code should be 200
    And the todo should no longer exist
