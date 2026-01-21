
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from main import app
from src.models import User, Review, PromptState, ReviewState

client = TestClient(app)

# Mocking the database
@patch("main.db")
def test_create_user(mock_db):
    mock_db.create_user.return_value = "test_user_id"
    
    user_data = {
        "id": "test_user_id",
        "name": "Test User",
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
    
    prompt_state = {
        "user_prompt": "test prompt",
        "review_columns": {}
    }
    
    review_data = {
        "id": "test_review_id",
        "user_id": "test_user_id",
        "collection_ids": [],
        "prompt_state": prompt_state,
        "review_states": []
    }
    
    response = client.post("/reviews", json=review_data)
    
    assert response.status_code == 201
    assert response.json() == {"message": "Review created successfully", "id": "test_review_id"}
    mock_db.create_review.assert_called_once()


@patch("main.db")
def test_update_review_prompt_state(mock_db):
    mock_db.update_review.return_value = True
    
    review_id = "test_review_id"
    prompt_state = {
        "user_prompt": "updated prompt",
        "review_columns": {"col1": "val1"}
    }
    
    review_data = {
        "id": review_id,
        "user_id": "test_user_id",
        "collection_ids": [],
        "prompt_state": prompt_state,
        "review_states": []
    }
    
    response = client.put(f"/reviews/{review_id}", json=review_data)
    
    assert response.status_code == 200
    assert response.json() == {"message": "Review updated successfully"}
    mock_db.update_review.assert_called_once()
    
    # Verify arguments
    args, _ = mock_db.update_review.call_args
    assert args[0] == review_id
    assert args[1].prompt_state.user_prompt == "updated prompt"
