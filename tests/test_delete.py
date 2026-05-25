def create_todo(client, title="Todo to delete"):
    resp = client.post("/todos/", json={"title": title})
    assert resp.status_code == 200
    return resp.json()


def test_delete_existing_todo(client):
    created = create_todo(client)
    todo_id = created["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Todo deleted"}


def test_read_after_delete(client):
    created = create_todo(client)
    todo_id = created["id"]

    del_response = client.delete(f"/todos/{todo_id}")
    assert del_response.status_code == 200

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Todo not found"}


def test_delete_todo_not_found(client):
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
