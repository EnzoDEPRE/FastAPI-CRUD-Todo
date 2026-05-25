"""
test_root.py — Tests for the root endpoint.

Manual test cases covered:
  - TC-001 : Health check (frontend served at /)
  - TC-001b : API info endpoint (/api)
"""


def test_root_serves_frontend(client):
    """
    TC-001 — GET / should return 200 and serve the HTML frontend.

    The root route was updated to serve the static index.html after
    the frontend was added. This test verifies the application is
    running and the frontend is accessible.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_api_info(client):
    """
    TC-001b — GET /api should return 200 and the welcome JSON message.

    The JSON welcome message was moved to /api to free up / for the frontend.
    """
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Enhanced FastAPI Todo App!"}
