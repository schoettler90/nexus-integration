# nexus-integration

## Prerequisites

### Install Python 3.13

#### Windows

1. Download Python 3.13 from the official website:
   - Visit [https://www.python.org/downloads/](https://www.python.org/downloads/)
   - Download the latest Python 3.13.x installer for Windows

2. Run the installer:
   - **Important**: Check "Add Python 3.13 to PATH" during installation
   - Click "Install Now" or choose "Customize installation" for advanced options

3. Verify the installation:
   ```powershell
   python --version
   ```
   Should output: `Python 3.13.x`

#### macOS

Using Homebrew:
```bash
brew install python@3.13
```

Or download from [python.org](https://www.python.org/downloads/)

#### Linux

Using apt (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3.13-dev
```

Using dnf (Fedora):
```bash
sudo dnf install python3.13
```

### Create and Activate Virtual Environment (Python 3.13)

#### macOS

1. Create a virtual environment with Python 3.13:
   ```bash
   python3.13 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Verify Python version in the virtual environment:
   ```bash
   python --version
   ```
   Should output: `Python 3.13.x`

#### Linux

1. Create a virtual environment with Python 3.13:
   ```bash
   python3.13 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Verify Python version in the virtual environment:
   ```bash
   python --version
   ```
   Should output: `Python 3.13.x`

#### Windows (PowerShell)

1. Create a virtual environment with Python 3.13:
   ```powershell
   python -m venv .venv
   ```

2. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   If you encounter an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. Verify Python version in the virtual environment:
   ```powershell
   python --version
   ```
   Should output: `Python 3.13.x`

### Install Poetry

Poetry is a dependency management and packaging tool for Python.

**Note**: Make sure your virtual environment is activated before installing Poetry.

#### All Platforms (macOS/Linux/Windows)

Install Poetry using pip:
```bash
pip install poetry
```

#### Verify Poetry Installation

```bash
poetry --version
```

#### Configure Poetry (Optional)

To create virtual environments inside the project directory:
```bash
poetry config virtualenvs.in-project true
```

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd nexus-integration
   ```

2. Create a `.env` file in the root directory with your MongoDB connection string:
   ```bash
   MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
   DATABASE_NAME=nexus_db
   ```

3. Install dependencies:
   ```bash
   poetry install
   ```

4. Activate the virtual environment:
   ```bash
   poetry shell
   ```

## Usage

### Running the API

Start the FastAPI server with uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at:
- **API Base URL**: http://localhost:8000
- **Interactive API Docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### API Endpoints

#### Users
- `POST /users` - Create a new user
- `GET /users` - List all users
- `GET /users/{user_id}` - Get a specific user
- `PUT /users/{user_id}` - Update a user
- `DELETE /users/{user_id}` - Delete a user

#### Collections
- `POST /collections` - Create a new collection
- `GET /collections` - List all collections
- `GET /collections/{collection_id}` - Get a specific collection
- `PUT /collections/{collection_id}` - Update a collection
- `DELETE /collections/{collection_id}` - Delete a collection
- `POST /collections/{collection_id}/documents/{document_id}` - Add a document to a collection
- `DELETE /collections/{collection_id}/documents/{document_id}` - Remove a document from a collection

#### Review States
- `POST /review-states` - Create a new review state
- `GET /review-states` - List all review states
- `GET /review-states/{review_id}` - Get a specific review state
- `PUT /review-states/{review_id}` - Update a review state
- `DELETE /review-states/{review_id}` - Delete a review state

#### Reviews
- `POST /reviews` - Create a new review
- `GET /reviews` - List all reviews
- `GET /reviews/{review_id}` - Get a specific review
- `PUT /reviews/{review_id}` - Update a review
- `DELETE /reviews/{review_id}` - Delete a review
- `GET /reviews/user/{user_id}` - Get all reviews by a specific user
- `POST /reviews/{review_id}/collections/{collection_id}` - Add a collection to a review
- `DELETE /reviews/{review_id}/collections/{collection_id}` - Remove a collection from a review
- `POST /reviews/{review_id}/review-states` - Add a review state to a review

#### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with database status

### Example Usage

#### Create a User
```bash
curl -X POST "http://localhost:8000/users" \
  -H "Content-Type: application/json" \
  -d '{"id": "user123", "name": "John Doe"}'
```

#### Get All Users
```bash
curl -X GET "http://localhost:8000/users"
```

#### Create a Collection
```bash
curl -X POST "http://localhost:8000/collections" \
  -H "Content-Type: application/json" \
  -d '{"id": "col123", "collection_name": "My Collection", "document_ids": []}'
```

For more detailed API documentation and to try out the endpoints interactively, visit http://localhost:8000/docs after starting the server.



