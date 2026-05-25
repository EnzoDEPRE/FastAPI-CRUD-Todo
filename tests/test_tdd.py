def test_tdd_f1_empty_title_rejected(client):
    response = client.post("/todos/", json={"title": ""})
    assert response.status_code == 422


def test_tdd_f2_filter_by_status(client):
    client.post("/todos/", json={"title": "Pending todo", "status": "pending"})
    client.post("/todos/", json={"title": "Done todo", "status": "done"})

    response = client.get("/todos/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "pending"
    assert data[0]["title"] == "Pending todo"


def test_tdd_f3_count_todos(client):
    client.post("/todos/", json={"title": "Todo 1"})
    client.post("/todos/", json={"title": "Todo 2"})
    client.post("/todos/", json={"title": "Todo 3"})

    response = client.get("/todos/count")
    assert response.status_code == 200
    assert response.json() == {"count": 3}
