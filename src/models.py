from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: str = Field(..., description="The unique identifier for the user")
    name: str = Field(..., description="The name of the user")
    email: str = Field(..., description="The email of the user")
    password: str = Field(..., description="The password of the user")
    review_ids: list[str] = Field(default_factory=list, description="The list of review ids")

class Collection(BaseModel):
    id: str = Field(..., description="The unique identifier for document collection")
    user_id: str = Field(..., description="The ID of the user who owns this collection")
    collection_name: str = Field(..., description="The name of the document collection")
    document_ids: list[str] = Field(default_factory=list, description="The list of document ids")

class Review(BaseModel):
    id: str = Field(..., description="The unique identifier for the review")
    user_id: str = Field(..., description="The unique identifier for the user who made the review")
    name: str = Field(..., description="The name of the review")
    prompt: Optional[str] = Field(None, description="The user prompt")
    collection_ids: list[str] = Field(default_factory=list, description="The list of collection ids")
    fields: list[dict] = Field(default_factory=list, description=" The schema of columns")
    results: list[dict] = Field(default_factory=list, description="The output results")
    runs: list[dict] = Field(default_factory=list, description="List of previous review runs")
    updated_at: Optional[str] = Field(None, description="ISO timestamp of last update")

class ReviewRun(BaseModel):
    id: str = Field(..., description="The unique identifier for the run")
    review_id: str = Field(..., description="The ID of the parent review")
    created_at: str = Field(..., description="ISO timestamp of creation")
    name: Optional[str] = Field(None, description="Name of the run")
    prompt: Optional[str] = Field(None, description="Snapshot of the prompt")
    collection_ids: list[str] = Field(default_factory=list, description="Snapshot of collection ids")
    fields: list[dict] = Field(default_factory=list, description="Snapshot of columns")
    results: list[dict] = Field(default_factory=list, description="The results of this run")
    status: str = Field(..., description="Run status (success, failed, etc)")
