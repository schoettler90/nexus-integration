from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: str = Field(..., description="The unique identifier for the user")
    name: str = Field(..., description="The name of the user")
    review_ids: list[str] = Field(default_factory=list, description="The list of review ids")

class Collection(BaseModel):
    id: str = Field(..., description="The unique identifier for document collection")
    collection_name: str = Field(..., description="The name of the document collection")
    document_ids: list[str] = Field(default_factory=list, description="The list of document ids")

class ReviewState(BaseModel):
    review_id: str = Field(..., description="The unique identifier for the review")
    date_created: int = Field(..., description="The date the review was created in epoch time")
    date_modified: int = Field(..., description="The date the review was last modified")
    user_prompt: Optional[str] = Field(None, description="The user prompt for the review")
    review_columns: Optional[list[dict]] = Field(default_factory=list, description="The list of review columns")
    reviews: list[dict] = Field(default_factory=list, description="The list of reviews")
    reviewed_ids: list[str] = Field(default_factory=list, description="The list of reviewed document ids")

class Review(BaseModel):
    id: int = Field(..., description="The unique identifier for the review")
    user_id: int = Field(..., description="The unique identifier for the user who made the review")
    collection_ids: list[str] = Field(default_factory=list, description="The list of collection ids")
    state: ReviewState = Field(..., description="The current state of the review")
    review_states: list[ReviewState] = Field(default_factory=list, description="The list of past reviewed states")



