# Nexus Integration API Documentation

## Overview

This FastAPI application provides a complete REST API for managing users, collections, reviews, and review states with MongoDB as the backend database.

## Architecture

### Components

1. **Models** (`src/models.py`): Pydantic models for data validation
   - User
   - Collection
   - PromptState
   - ReviewState
   - Review

2. **Database Layer** (`src/mongodb.py`): MongoDB CRUD operations
   - MongoDB class with methods for all database operations
   - Connection lifecycle management

3. **API Layer** (`main.py`): FastAPI endpoints
   - RESTful API endpoints for all operations
   - Request/response validation
   - Error handling

## API Endpoints

### Users

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/users` | Create a new user | `User` | `{"message": "string", "id": "string"}` |
| GET | `/users` | List all users | - | `[User]` |
| GET | `/users/{user_id}` | Get a specific user | - | `User` |
| PUT | `/users/{user_id}` | Update a user | `User` | `{"message": "string"}` |
| DELETE | `/users/{user_id}` | Delete a user | - | `{"message": "string"}` |

### Collections

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/collections` | Create a new collection | `Collection` | `{"message": "string", "id": "string"}` |
| GET | `/collections` | List all collections | - | `[Collection]` |
| GET | `/collections/{collection_id}` | Get a specific collection | - | `Collection` |
| PUT | `/collections/{collection_id}` | Update a collection | `Collection` | `{"message": "string"}` |
| DELETE | `/collections/{collection_id}` | Delete a collection | - | `{"message": "string"}` |
| POST | `/collections/{collection_id}/documents/{document_id}` | Add document to collection | - | `{"message": "string"}` |
| DELETE | `/collections/{collection_id}/documents/{document_id}` | Remove document from collection | - | `{"message": "string"}` |

### Review States

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/review-states` | Create a new review state | `ReviewState` | `{"message": "string", "id": "string"}` |
| GET | `/review-states` | List all review states | - | `[ReviewState]` |
| GET | `/review-states/{review_id}` | Get a specific review state | - | `ReviewState` |
| PUT | `/review-states/{review_id}` | Update a review state | `ReviewState` | `{"message": "string"}` |
| DELETE | `/review-states/{review_id}` | Delete a review state | - | `{"message": "string"}` |

### Reviews

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/reviews` | Create a new review | `Review` | `{"message": "string", "id": "string"}` |
| GET | `/reviews` | List all reviews | - | `[Review]` |
| GET | `/reviews/{review_id}` | Get a specific review | - | `Review` |
| PUT | `/reviews/{review_id}` | Update a review | `Review` | `{"message": "string"}` |
| DELETE | `/reviews/{review_id}` | Delete a review | - | `{"message": "string"}` |
| GET | `/reviews/user/{user_id}` | Get all reviews by a user | - | `[Review]` |
| POST | `/reviews/{review_id}/collections/{collection_id}` | Add collection to review | - | `{"message": "string"}` |
| DELETE | `/reviews/{review_id}/collections/{collection_id}` | Remove collection from review | - | `{"message": "string"}` |
| POST | `/reviews/{review_id}/review-states` | Add review state to review | `ReviewState` | `{"message": "string"}` |

### Health Check

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Basic health check | `{"message": "string", "status": "string"}` |
| GET | `/health` | Detailed health check | `{"status": "string", "database": "string"}` |

## Data Models

### User
```json
{
  "id": "string",
  "name": "string",
  "review_ids": ["string"]
}
```

### Collection
```json
{
  "id": "string",
  "collection_name": "string",
  "document_ids": ["string"]
}
```

### PromptState
```json
{
  "user_prompt": "string",
  "review_columns": {}
}
```

### ReviewState
```json
{
  "review_id": "string",
  "date_created": 0,
  "date_modified": 0,
  "prompt_state": {
    "user_prompt": "string",
    "review_columns": {}
  },
  "reviews": [{}],
  "reviewed_ids": ["string"]
}
```

### Review
```json
{
  "id": "string",
  "user_id": "string",
  "collection_ids": ["string"],
  "prompt_state": {
    "user_prompt": "string",
    "review_columns": {}
  },
  "review_states": [
    {
      "review_id": "string",
      "date_created": 0,
      "date_modified": 0,
      "prompt_state": {
        "user_prompt": "string",
        "review_columns": {}
      },
      "reviews": [{}],
      "reviewed_ids": ["string"]
    }
  ]
}
```

## MongoDB Methods

All MongoDB CRUD operations are available in the `MongoDB` class:

### User Operations
- `create_user(user: User) -> str`
- `get_user(user_id: str) -> Optional[User]`
- `update_user(user_id: str, user: User) -> bool`
- `delete_user(user_id: str) -> bool`
- `list_users() -> List[User]`

### Collection Operations
- `create_collection(collection: Collection) -> str`
- `get_collection(collection_id: str) -> Optional[Collection]`
- `update_collection(collection_id: str, collection: Collection) -> bool`
- `delete_collection(collection_id: str) -> bool`
- `list_collections() -> List[Collection]`
- `add_document_to_collection(collection_id: str, document_id: str) -> bool`
- `remove_document_from_collection(collection_id: str, document_id: str) -> bool`

### ReviewState Operations
- `create_review_state(review_state: ReviewState) -> str`
- `get_review_state(review_id: str) -> Optional[ReviewState]`
- `update_review_state(review_id: str, review_state: ReviewState) -> bool`
- `delete_review_state(review_id: str) -> bool`
- `list_review_states() -> List[ReviewState]`

### Review Operations
- `create_review(review: Review) -> str`
- `get_review(review_id: str) -> Optional[Review]`
- `update_review(review_id: str, review: Review) -> bool`
- `delete_review(review_id: str) -> bool`
- `list_reviews() -> List[Review]`
- `get_reviews_by_user(user_id: str) -> List[Review]`
- `add_collection_to_review(review_id: str, collection_id: str) -> bool`
- `remove_collection_from_review(review_id: str, collection_id: str) -> bool`
- `add_review_state_to_review(review_id: str, review_state: ReviewState) -> bool`

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Database connection issue

## Running the API

1. Make sure MongoDB is configured in `.env`:
   ```
   MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=nexus_db
   ```

2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

3. Access the interactive documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Example API Calls

### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user123",
    "name": "John Doe",
    "review_ids": []
  }'
```

### Get All Users
```bash
curl -X GET "http://localhost:8000/users"
```

### Create a Collection
```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "col123",
    "collection_name": "My Collection",
    "document_ids": ["doc1", "doc2"]
  }'
```

### Add Document to Collection
```bash
curl -X POST "http://localhost:8000/collections/col123/documents/doc3"
```

### Create a Review State
```bash
curl -X POST "http://localhost:8000/review-states" \
  -H "Content-Type: application/json" \
  -d '{
    "review_id": "review123",
    "date_created": 1737360000,
    "date_modified": 1737360000,
    "prompt_state": {
      "user_prompt": "Analyze this",
      "review_columns": {}
    },
    "reviews": [],
    "reviewed_ids": []
  }'
```

### Create a Review
```bash
curl -X POST "http://localhost:8000/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "review101",
    "user_id": "user123",
    "collection_ids": ["col123"],
    "prompt_state": {
      "user_prompt": "Initial prompt",
      "review_columns": {}
    },
    "review_states": []
  }'
```

### Get Reviews by User
```bash
curl -X GET "http://localhost:8000/reviews/user/user123"
```
