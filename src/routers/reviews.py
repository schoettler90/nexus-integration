from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from src.models import Review
from src.routers.deps import get_db

router = APIRouter(tags=["Reviews"])


@router.post("/reviews", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_review(review: Review):
    """Create a new review."""
    try:
        review_id = get_db().create_review(review)
        return {"message": "Review created successfully", "id": review_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    """Get a review by ID."""
    review = get_db().get_review(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return review


@router.get("/reviews", response_model=List[Review])
async def list_reviews(user_id: Optional[str] = None):
    """Get all reviews, optionally filtered by user_id."""
    try:
        return get_db().list_reviews(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.put("/reviews/{review_id}", response_model=dict)
async def update_review(review_id: str, review: Review):
    """Update an existing review."""
    success = get_db().update_review(review_id, review)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found or no changes made",
        )
    return {"message": "Review updated successfully"}


@router.delete("/reviews/{review_id}", response_model=dict)
async def delete_review(review_id: str):
    """Delete a review by ID."""
    success = get_db().delete_review(review_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Review not found"
        )
    return {"message": "Review deleted successfully"}
