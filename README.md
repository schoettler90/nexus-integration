# Nexus Integration API

## Overview

Nexus Integration API is a FastAPI-based application designed to manage the lifecycle of document reviews. It serves as a central hub for:

- **User Management**: Handling user identities (bcrypt-hashed passwords, `/login`) and their associated reviews.
- **Collection Management**: Organizing documents into specific collections for targeted processing.
- **Review System**: Orchestrating the review process, where users can create reviews for collections, tracking the state of prompt execution.

This API is built with a focus on reliability and clarity, utilizing MongoDB for persistent storage and Pydantic for strict data validation. Full endpoint reference: [API_DOCUMENTATION.md](API_DOCUMENTATION.md).

## Prerequisites

### Install uv

[uv](https://docs.astral.sh/uv/) manages the Python toolchain and dependencies
(it installs a suitable Python automatically):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS / Linux
# or: brew install uv
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nexus-integration
   ```

2. **Configure Environment**:
   Create a `.env` file in the root directory:
   ```env
   MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=nexus_db
   ```

3. **Install Dependencies**:
   ```bash
   uv sync
   ```

## Usage

### Running the API

Start the server using Uvicorn (port 8001 — nexus-backend owns `:8000`):

```bash
uv run uvicorn main:app --reload --port 8001
```

The API will be available at:
- **Base URL**: http://localhost:8001
- **Documentation**: http://localhost:8001/docs

### Running the tests

```bash
uv run pytest
```

### API Endpoints Summary

- **Users**: Create, read, update, delete users; `/login` for authentication. User responses never include the password.
- **Collections**: Manage document collections (add/remove documents).
- **Reviews**: Create reviews linking users to collections and prompts.

### Example Usage

#### Create a User
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

#### Log In
```bash
curl -X POST "http://localhost:8001/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com", "password": "a-strong-password"}'
```

#### Create a Collection
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

#### Create a Review
```bash
curl -X POST "http://localhost:8001/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "review101",
    "user_id": "user123",
    "name": "Initial review",
    "prompt": "Initial analysis prompt",
    "collection_ids": ["col123"]
  }'
```

## Migrating pre-existing plaintext passwords

Existing user records created before password hashing landed can be migrated
in place (idempotent — already-hashed records are skipped):

```bash
uv run python scripts/hash_passwords.py
```

## Health Check

- **Basic**: `GET /`
- **Detailed**: `GET /health` (checks MongoDB connection)
