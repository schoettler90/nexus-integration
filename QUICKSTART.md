# Quick Start Guide

## Prerequisites
- Python 3.13 installed
- MongoDB Atlas account (or local MongoDB instance)

## Setup (5 minutes)

### 1. Create and activate virtual environment

**macOS/Linux:**
```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install Poetry and dependencies
```bash
pip install poetry
poetry install
```

### 3. Configure environment variables

Create a `.env` file in the project root:
```bash
MONGODB_ATLAS_CLUSTER_URI=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=nexus_db
```

Replace `username`, `password`, and `cluster` with your MongoDB credentials.

### 4. Start the API server
```bash
uvicorn main:app --reload
```

### 5. Access the API

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **API Documentation**: http://localhost:8000/redoc

## Test the API

Open http://localhost:8000/docs in your browser and try these operations:

1. **Create a User**
   - Click on `POST /users`
   - Click "Try it out"
   - Enter: `{"id": "user1", "name": "John Doe"}`
   - Click "Execute"

2. **Get All Users**
   - Click on `GET /users`
   - Click "Try it out"
   - Click "Execute"

3. **Check Health**
   - Click on `GET /health`
   - Click "Try it out"
   - Click "Execute"

## Project Structure

```
nexus-integration/
├── main.py                 # FastAPI application with all endpoints
├── src/
│   ├── models.py          # Pydantic data models
│   ├── mongodb.py         # MongoDB CRUD operations
│   └── __init__.py
├── .env                   # Environment variables (create this)
├── .env.example           # Environment template
├── pyproject.toml         # Project dependencies
├── README.md              # Full documentation
└── API_DOCUMENTATION.md   # Complete API reference
```

## What's Available?

✅ **27 API Endpoints** across 5 categories:
- Users (5 endpoints)
- Collections (7 endpoints)
- Review States (5 endpoints)
- Reviews (9 endpoints)
- Health Check (2 endpoints)

✅ **Complete CRUD Operations** for all models:
- Create, Read, Update, Delete for Users, Collections, ReviewStates, and Reviews
- Additional helper methods for managing relationships

✅ **MongoDB Integration** with connection lifecycle management

✅ **Interactive API Documentation** with Swagger UI

## Need Help?

- See `README.md` for detailed installation instructions
- See `API_DOCUMENTATION.md` for complete API reference
- Visit http://localhost:8000/docs for interactive API testing

## Common Issues

**Issue**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure you've run `poetry install` and activated the virtual environment

**Issue**: `pymongo.errors.ConfigurationError`
**Solution**: Check your MongoDB connection string in `.env` file

**Issue**: Port 8000 already in use
**Solution**: Run with a different port: `uvicorn main:app --reload --port 8001`

