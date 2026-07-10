from fastapi import APIRouter, HTTPException, status
from typing import List, Optional

from src.models import Collection
from src.routers.deps import get_db

router = APIRouter(tags=["Collections"])


@router.post("/collections", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_collection(collection: Collection):
    """Create a new collection."""
    try:
        collection_id = get_db().create_collection(collection)
        return {"message": "Collection created successfully", "id": collection_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/collections/{collection_id}", response_model=Collection)
async def get_collection(collection_id: str):
    """Get a collection by ID."""
    collection = get_db().get_collection(collection_id)
    if not collection:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return collection


@router.put("/collections/{collection_id}", response_model=dict)
async def update_collection(collection_id: str, collection: Collection):
    """Update an existing collection."""
    success = get_db().update_collection(collection_id, collection)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found or no changes made",
        )
    return {"message": "Collection updated successfully"}


@router.delete("/collections/{collection_id}", response_model=dict)
async def delete_collection(collection_id: str):
    """Delete a collection by ID."""
    success = get_db().delete_collection(collection_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return {"message": "Collection deleted successfully"}


@router.post(
    "/collections/{collection_id}/documents/{document_id}", response_model=dict
)
async def add_document_to_collection(collection_id: str, document_id: str):
    """Add a document to a collection."""
    success = get_db().add_document_to_collection(collection_id, document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Collection not found"
        )
    return {"message": "Document added to collection successfully"}


@router.delete(
    "/collections/{collection_id}/documents/{document_id}", response_model=dict
)
async def remove_document_from_collection(collection_id: str, document_id: str):
    """Remove a document ID from a collection."""
    success = get_db().remove_document_from_collection(collection_id, document_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found or document doesn't exist",
        )
    return {"message": "Document removed from collection successfully"}


@router.get("/collections", response_model=List[Collection])
async def list_collections(user_id: Optional[str] = None):
    """Get all collections, optionally filtered by user_id."""
    try:
        return get_db().list_collections(user_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
