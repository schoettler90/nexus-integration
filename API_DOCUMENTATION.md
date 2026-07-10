# Nexus Integration API Documentation

## Overview

This FastAPI application provides a REST API for managing users, collections, and
reviews with MongoDB as the backend database. It listens on port **8001**
(nexus-backend owns `:8000`).

## Architecture

### Components

1. **Models** (`src/models.py`): Pydantic models for data validation
   - `User` (request model; the stored password is a bcrypt hash)
   - `UserPublic` (response model — never includes `password`)
   - `Collection`
   - `Review`

2. **Security** (`src/security.py`): bcrypt password hashing
   - `hash_password`, `verify_password`, `is_bcrypt_hash`

3. **Database Layer** (`src/mongodb.py`): MongoDB CRUD operations
   - `MongoDB` class with methods for all database operations
   - Connection lifecycle management

4. **API Layer** (`main.py` + `src/routers/`): FastAPI endpoints
   - `main.py` — app wiring, CORS, lifespan, `/` and `/health`
   - `src/routers/users.py`, `src/routers/collections.py`,
     `src/routers/reviews.py` — the resource endpoints

## API Endpoints

### Users

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/users` | Create a new user (password bcrypt-hashed) | `User` | `{"message": "string", "id": "string"}` |
| POST | `/login` | Authenticate a user | `{"email": "string", "password": "string"}` | `{"message": "string", "user_id": "string", "name": "string"}` (401 on bad credentials) |
| GET | `/users` | List all users | - | `[UserPublic]` |
| GET | `/users/{user_id}` | Get a specific user | - | `UserPublic` |
| PUT | `/users/{user_id}` | Update a user (a new plaintext password is hashed) | `User` | `{"message": "string"}` |
| DELETE | `/users/{user_id}` | Delete a user | - | `{"message": "string"}` |

### Collections

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/collections` | Create a new collection | `Collection` | `{"message": "string", "id": "string"}` |
| GET | `/collections` | List all collections (optional `?user_id=`) | - | `[Collection]` |
| GET | `/collections/{collection_id}` | Get a specific collection | - | `Collection` |
| PUT | `/collections/{collection_id}` | Update a collection | `Collection` | `{"message": "string"}` |
| DELETE | `/collections/{collection_id}` | Delete a collection | - | `{"message": "string"}` |
| POST | `/collections/{collection_id}/documents/{document_id}` | Add document to collection | - | `{"message": "string"}` |
| DELETE | `/collections/{collection_id}/documents/{document_id}` | Remove document from collection | - | `{"message": "string"}` |

### Reviews

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| POST | `/reviews` | Create a new review | `Review` | `{"message": "string", "id": "string"}` |
| GET | `/reviews` | List all reviews (optional `?user_id=`) | - | `[Review]` |
| GET | `/reviews/{review_id}` | Get a specific review | - | `Review` |
| PUT | `/reviews/{review_id}` | Update a review | `Review` | `{"message": "string"}` |
| DELETE | `/reviews/{review_id}` | Delete a review | - | `{"message": "string"}` |

### Health Check

| Method | Endpoint | Description | Response |
|--------|----------|-------------|----------|
| GET | `/` | Basic health check | `{"message": "string", "status": "string"}` |
| GET | `/health` | Detailed health check | `{"status": "string", "database": "string"}` |

## Data Models

### User (request)
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "password": "string",
  "review_ids": ["string"]
}
```

### UserPublic (response — no password)
```json
{
  "id": "string",
  "name": "string",
  "email": "string",
  "review_ids": ["string"]
}
```

### Collection
```json
{
  "id": "string",
  "user_id": "string",
  "collection_name": "string",
  "document_ids": ["string"]
}
```

### Review
```json
{
  "id": "string",
  "user_id": "string",
  "name": "string",
  "prompt": "string",
  "collection_ids": ["string"],
  "fields": [{}],
  "results": [{}],
  "runs": [{}],
  "updated_at": "string"
}
```

## MongoDB Methods

All MongoDB CRUD operations are available in the `MongoDB` class:

### User Operations
- `create_user(user: User) -> str`
- `get_user(user_id: str) -> Optional[User]`
- `get_user_by_email(email: str) -> Optional[User]`
- `update_user(user_id: str, user: User) -> bool`
- `delete_user(user_id: str) -> bool`
- `list_users() -> List[User]`

### Collection Operations
- `create_collection(collection: Collection) -> str`
- `get_collection(collection_id: str) -> Optional[Collection]`
- `update_collection(collection_id: str, collection: Collection) -> bool`
- `delete_collection(collection_id: str) -> bool`
- `list_collections(user_id: Optional[str]) -> List[Collection]`
- `add_document_to_collection(collection_id: str, document_id: str) -> bool`
- `remove_document_from_collection(collection_id: str, document_id: str) -> bool`

### Review Operations
- `create_review(review: Review) -> str`
- `get_review(review_id: str) -> Optional[Review]`
- `update_review(review_id: str, review: Review) -> bool`
- `delete_review(review_id: str) -> bool`
- `list_reviews(user_id: Optional[str]) -> List[Review]`

## Error Handling

The API uses standard HTTP status codes:

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `401 Unauthorized` - Invalid login credentials
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Database connection issue

## Running the API

1. Make sure MongoDB is configured in `.env`:
   ```
   MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=nexus_db
   ```

2. Install dependencies and start the server (port 8001):
   ```bash
   uv sync
   uv run uvicorn main:app --reload --port 8001
   ```

3. Access the interactive documentation:
   - Swagger UI: http://localhost:8001/docs
   - ReDoc: http://localhost:8001/redoc

## Scripts

- `scripts/create_user.py` — create a user from the CLI
  (`uv run python scripts/create_user.py --id u1 --name Jane --email jane@example.com`;
  prompts for the password and stores its bcrypt hash).
- `scripts/hash_passwords.py` — one-time migration hashing pre-existing
  plaintext passwords; idempotent (already-hashed records are skipped).
- `scripts/verify_user.py` — fetch and print a user record.

## Example API Calls

### Create a User
```bash
curl -X POST "http://localhost:8001/users" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user123",
    "name": "John Doe",
    "email": "john@example.com",
    "password": "a-strong-password",
    "review_ids": []
  }'
```

### Log In
```bash
curl -X POST "http://localhost:8001/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "a-strong-password"}'
```

### Get All Users
```bash
curl -X GET "http://localhost:8001/users"
```

### Create a Collection
```bash
curl -X POST "http://localhost:8001/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "col123",
    "user_id": "user123",
    "collection_name": "My Collection",
    "document_ids": ["doc1", "doc2"]
  }'
```

### Add Document to Collection
```bash
curl -X POST "http://localhost:8001/collections/col123/documents/doc3"
```

### Create a Review
```bash
curl -X POST "http://localhost:8001/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "review101",
    "user_id": "user123",
    "name": "Initial review",
    "prompt": "Initial prompt",
    "collection_ids": ["col123"]
  }'
```

### Get Reviews by User
```bash
curl -X GET "http://localhost:8001/reviews?user_id=user123"
```
