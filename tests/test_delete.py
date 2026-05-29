def test_user_can_delete_an_existing_todo(client, create_todo):
    created = create_todo(title="Todo to delete")
    todo_id = created["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"detail": "Todo deleted"}


def test_deleted_todo_can_no_longer_be_read(client, create_todo):
    created = create_todo(title="Todo to delete")
    todo_id = created["id"]

    del_response = client.delete(f"/todos/{todo_id}")
    assert del_response.status_code == 200

    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Todo not found"}


def test_user_gets_404_when_deleting_an_unknown_todo(client):
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
