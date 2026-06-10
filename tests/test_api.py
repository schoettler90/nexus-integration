
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

# Mocking the database
@patch("main.db")
def test_create_user(mock_db):
    mock_db.create_user.return_value = "test_user_id"

    user_data = {
        "id": "test_user_id",
        "name": "Test User",
        "email": "test@example.com",
        "password": "secret",
        "review_ids": []
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201
    assert response.json() == {"message": "User created successfully", "id": "test_user_id"}
    mock_db.create_user.assert_called_once()


@patch("main.db")
def test_update_user(mock_db):
    mock_db.update_user.return_value = True

    user_id = "test_user_id"
    user_data = {
        "id": user_id,
        "name": "Updated Test User",
        "email": "test@example.com",
        "password": "secret",
        "review_ids": ["review_1"]
    }

    response = client.put(f"/users/{user_id}", json=user_data)

    assert response.status_code == 200
    assert response.json() == {"message": "User updated successfully"}
    mock_db.update_user.assert_called_once()

    # Verify arguments
    args, _ = mock_db.update_user.call_args
    assert args[0] == user_id
    assert args[1].name == "Updated Test User"


@patch("main.db")
def test_create_review(mock_db):
    mock_db.create_review.return_value = "test_review_id"

    review_data = {
        "id": "test_review_id",
        "user_id": "test_user_id",
        "name": "Test Review",
        "prompt": "test prompt",
        "collection_ids": [],
        "fields": [],
        "results": [],
        "runs": []
    }

    response = client.post("/reviews", json=review_data)

    assert response.status_code == 201
    assert response.json() == {"message": "Review created successfully", "id": "test_review_id"}
    mock_db.create_review.assert_called_once()


@patch("main.db")
def test_update_review_prompt(mock_db):
    mock_db.update_review.return_value = True

    review_id = "test_review_id"
    review_data = {
        "id": review_id,
        "user_id": "test_user_id",
        "name": "Test Review",
        "prompt": "updated prompt",
        "collection_ids": [],
        "fields": [{"name": "col1", "type": "string"}],
        "results": [],
        "runs": []
    }

    response = client.put(f"/reviews/{review_id}", json=review_data)

    assert response.status_code == 200
    assert response.json() == {"message": "Review updated successfully"}
    mock_db.update_review.assert_called_once()

    # Verify arguments
    args, _ = mock_db.update_review.call_args
    assert args[0] == review_id
    assert args[1].prompt == "updated prompt"


@patch("main.db")
def test_login_success(mock_db):
    user = type("U", (), {"id": "u1", "name": "Test User", "password": "secret"})()
    mock_db.get_user_by_email.return_value = user

    response = client.post("/login", json={"email": "test@example.com", "password": "secret"})

    assert response.status_code == 200
    assert response.json() == {"message": "Login successful", "user_id": "u1", "name": "Test User"}


@patch("main.db")
def test_login_wrong_password(mock_db):
    user = type("U", (), {"id": "u1", "name": "Test User", "password": "secret"})()
    mock_db.get_user_by_email.return_value = user

    response = client.post("/login", json={"email": "test@example.com", "password": "wrong"})

    assert response.status_code == 401
