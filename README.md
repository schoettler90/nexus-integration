# Nexus Integration API

## Overview

Nexus Integration API is a robust FastAPI-based application designed to manage the lifecycle of document reviews. It serves as a central hub for:

- **User Management**: Handling user identities and their associated reviews.
- **Collection Management**: Organizing documents into specific collections for targeted processing.
- **Review System**: Orchestrating the review process, where users can create reviews for collections, tracking the state of prompt execution.
- **Review State Tracking**: capturing snapshots of review executions, including the exact prompt state used and the resulting output, allowing for historical auditing and comparison.

This API is built with a focus on reliability and clarity, utilizing MongoDB for persistent storage and Pydantic for strict data validation.

## Prerequisites

### Install Python 3.13

#### Windows

1. Download Python 3.13 from [python.org](https://www.python.org/downloads/).
2. Run the installer and **ensure "Add Python 3.13 to PATH" is checked**.
3. Verify: `python --version`

#### macOS

Using Homebrew:
```bash
brew install python@3.13
```

#### Linux

Using apt (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

### Install Poetry

Poetry is used for dependency management.

```bash
pip install poetry
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
   poetry install
   ```

4. **Activate Shell**:
   ```bash
   poetry shell
   ```

## Usage

### Running the API

Start the server using Uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **Base URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs

### API Endpoints Summary

- **Users**: Create, read, update, delete users.
- **Collections**: Manage document collections (add/remove documents).
- **Reviews**: Create reviews linking users to collections and prompts.
- **Review States**: specific snapshots of a review execution.

### Example Usage

#### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "user123",
    "name": "John Doe",
    "review_ids": []
  }'
```

#### Create a Collection
```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "col123",
    "collection_name": "My Collection",
    "document_ids": ["doc1", "doc2"]
  }'
```

#### Create a Review State
*Note: `prompt_state` is required.*
```bash
curl -X POST "http://localhost:8000/review-states" \
  -H "Content-Type: application/json" \
  -d '{
    "review_id": "review123",
    "date_created": 1737360000,
    "date_modified": 1737360000,
    "prompt_state": {
      "user_prompt": "Analyze this document for sentiment.",
      "review_columns": {}
    },
    "reviews": [],
    "reviewed_ids": []
  }'
```

#### Create a Review
*Note: `prompt_state` is required.*
```bash
curl -X POST "http://localhost:8000/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "review101",
    "user_id": "user123",
    "collection_ids": ["col123"],
    "prompt_state": {
      "user_prompt": "Initial analysis prompt",
      "review_columns": {}
    },
    "review_states": []
  }'
```

#### Get Reviews by User
```bash
curl -X GET "http://localhost:8000/reviews/user/user123"
```

## Health Check

- **Basic**: `GET /`
- **detailed**: `GET /health` (checks MongoDB connection)
