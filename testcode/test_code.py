from fastapi.testclient import TestClient
from performance_test import api  # adjust import path to your file

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}


def test_add_book():
    book_data = {
        "id": 1,
        "name": "Test Book",
        "description": "This is a test book",
        "isAvailable": True
    }
    response = client.post("/book", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert any(book["id"] == 1 for book in data)


def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_update_book():
    updated_data = {
        "id": 1,
        "name": "Updated Book",
        "description": "Updated description",
        "isAvailable": False
    }
    response = client.put("/book/1", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Book"
    assert data["isAvailable"] is False


def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

    # Confirm deletion
    response_check = client.get("/book")
    assert all(book["id"] != 1 for book in response_check.json())
