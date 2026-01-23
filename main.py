from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager

from src.mongodb import MongoDB
from src.models import User, Collection, ReviewState, Review


# MongoDB instance
db: Optional[MongoDB] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage MongoDB connection lifecycle."""
    global db
    db = MongoDB()
    yield
    db.close()


app = FastAPI(
    title="Nexus Integration API",
    description="API for managing users, collections, reviews, and review states",
    version="1.0.0",
    lifespan=lifespan
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for prototype
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==================== User Endpoints ====================

@app.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Users"])
async def create_user(user: User):
    """Create a new user."""
    try:
        user_id = db.create_user(user)
        return {"message": "User created successfully", "id": user_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/login", response_model=dict, tags=["Users"])
async def login(login_request: LoginRequest):
    """Authenticate a user."""
    user = db.get_user_by_email(login_request.email)
    if not user or user.password != login_request.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    return {"message": "Login successful", "user_id": user.id, "name": user.name}


@app.get("/users/{user_id}", response_model=User, tags=["Users"])
async def get_user(user_id: str):
    """Get a user by ID."""
    user = db.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@app.put("/users/{user_id}", response_model=dict, tags=["Users"])
async def update_user(user_id: str, user: User):
    """Update an existing user."""
    success = db.update_user(user_id, user)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or no changes made")
    return {"message": "User updated successfully"}


@app.delete("/users/{user_id}", response_model=dict, tags=["Users"])
async def delete_user(user_id: str):
    """Delete a user by ID."""
    success = db.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"message": "User deleted successfully"}


@app.get("/users", response_model=List[User], tags=["Users"])
async def list_users():
    """Get all users."""
    try:
        users = db.list_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Collection Endpoints ====================

@app.post("/collections", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Collections"])
async def create_collection(collection: Collection):
    """Create a new collection."""
    try:
        collection_id = db.create_collection(collection)
        return {"message": "Collection created successfully", "id": collection_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/collections/{collection_id}", response_model=Collection, tags=["Collections"])
async def get_collection(collection_id: str):
    """Get a collection by ID."""
    collection = db.get_collection(collection_id)
    if not collection:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return collection


@app.put("/collections/{collection_id}", response_model=dict, tags=["Collections"])
async def update_collection(collection_id: str, collection: Collection):
    """Update an existing collection."""
    success = db.update_collection(collection_id, collection)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found or no changes made")
    return {"message": "Collection updated successfully"}


@app.delete("/collections/{collection_id}", response_model=dict, tags=["Collections"])
async def delete_collection(collection_id: str):
    """Delete a collection by ID."""
    success = db.delete_collection(collection_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return {"message": "Collection deleted successfully"}


@app.post("/collections/{collection_id}/documents/{document_id}", response_model=dict, tags=["Collections"])
async def add_document_to_collection(collection_id: str, document_id: str):
    """Add a document to a collection."""
    success = db.add_document_to_collection(collection_id, document_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found")
    return {"message": "Document added to collection successfully"}


@app.get("/collections", response_model=List[Collection], tags=["Collections"])
async def list_collections(user_id: Optional[str] = None):
    """Get all collections, optionally filtered by user_id."""
    try:
        collections = db.list_collections(user_id)
        return collections
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/collections/{collection_id}/documents/{document_id}", response_model=dict, tags=["Collections"])
async def add_document_to_collection(collection_id: str, document_id: str):
    """Add a document ID to a collection."""
    success = db.add_document_to_collection(collection_id, document_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found or document already exists")
    return {"message": "Document added to collection successfully"}


@app.delete("/collections/{collection_id}/documents/{document_id}", response_model=dict, tags=["Collections"])
async def remove_document_from_collection(collection_id: str, document_id: str):
    """Remove a document ID from a collection."""
    success = db.remove_document_from_collection(collection_id, document_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found or document doesn't exist")
    return {"message": "Document removed from collection successfully"}


# ==================== ReviewState Endpoints ====================

@app.post("/review-states", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Review States"])
async def create_review_state(review_state: ReviewState):
    """Create a new review state."""
    try:
        review_state_id = db.create_review_state(review_state)
        return {"message": "Review state created successfully", "id": review_state_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/review-states/{review_id}", response_model=ReviewState, tags=["Review States"])
async def get_review_state(review_id: str):
    """Get a review state by review ID."""
    review_state = db.get_review_state(review_id)
    if not review_state:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review state not found")
    return review_state


@app.put("/review-states/{review_id}", response_model=dict, tags=["Review States"])
async def update_review_state(review_id: str, review_state: ReviewState):
    """Update an existing review state."""
    success = db.update_review_state(review_id, review_state)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review state not found or no changes made")
    return {"message": "Review state updated successfully"}


@app.delete("/review-states/{review_id}", response_model=dict, tags=["Review States"])
async def delete_review_state(review_id: str):
    """Delete a review state by review ID."""
    success = db.delete_review_state(review_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review state not found")
    return {"message": "Review state deleted successfully"}


@app.get("/review-states", response_model=List[ReviewState], tags=["Review States"])
async def list_review_states():
    """Get all review states."""
    try:
        review_states = db.list_review_states()
        return review_states
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# ==================== Review Endpoints ====================

@app.post("/reviews", response_model=dict, status_code=status.HTTP_201_CREATED, tags=["Reviews"])
async def create_review(review: Review):
    """Create a new review."""
    try:
        review_id = db.create_review(review)
        return {"message": "Review created successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/reviews/{review_id}", response_model=Review, tags=["Reviews"])
async def get_review(review_id: str):
    """Get a review by ID."""
    review = db.get_review(review_id)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return review


@app.put("/reviews/{review_id}", response_model=dict, tags=["Reviews"])
async def update_review(review_id: str, review: Review):
    """Update an existing review."""
    success = db.update_review(review_id, review)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or no changes made")
    return {"message": "Review updated successfully"}


@app.delete("/reviews/{review_id}", response_model=dict, tags=["Reviews"])
async def delete_review(review_id: str):
    """Delete a review by ID."""
    success = db.delete_review(review_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return {"message": "Review deleted successfully"}


@app.get("/reviews", response_model=List[Review], tags=["Reviews"])
async def list_reviews():
    """Get all reviews."""
    try:
        reviews = db.list_reviews()
        return reviews
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.get("/reviews/user/{user_id}", response_model=List[Review], tags=["Reviews"])
async def get_reviews_by_user(user_id: str):
    """Get all reviews for a specific user."""
    try:
        reviews = db.get_reviews_by_user(user_id)
        return reviews
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@app.post("/reviews/{review_id}/collections/{collection_id}", response_model=dict, tags=["Reviews"])
async def add_collection_to_review(review_id: str, collection_id: str):
    """Add a collection ID to a review."""
    success = db.add_collection_to_review(review_id, collection_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or collection already exists")
    return {"message": "Collection added to review successfully"}


@app.delete("/reviews/{review_id}/collections/{collection_id}", response_model=dict, tags=["Reviews"])
async def remove_collection_from_review(review_id: str, collection_id: str):
    """Remove a collection ID from a review."""
    success = db.remove_collection_from_review(review_id, collection_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or collection doesn't exist")
    return {"message": "Collection removed from review successfully"}


@app.post("/reviews/{review_id}/review-states", response_model=dict, tags=["Reviews"])
async def add_review_state_to_review(review_id: str, review_state: ReviewState):
    """Add a review state to a review's review_states list."""
    success = db.add_review_state_to_review(review_id, review_state)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    return {"message": "Review state added to review successfully"}


# ==================== Health Check ====================

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"message": "Nexus Integration API is running", "status": "healthy"}


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    try:
        # Test MongoDB connection
        db.list_users()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "database": "disconnected", "error": str(e)}
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
