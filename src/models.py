from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: str = Field(..., description="The unique identifier for the user")
    name: str = Field(..., description="The name of the user")

class Collection(BaseModel):
    id: str = Field(..., description="The unique identifier for the collection")
    collection_name: str = Field(..., description="The name of the collection")
    document_ids: list[str] = Field(default_factory=list, description="The list of document ids")


class ReviewState(BaseModel):
    review_id: str = Field(..., description="The unique identifier for the review")
    date_created: int = Field(..., description="The date the review was created in epoch time")
    date_modified: int = Field(..., description="The date the review was last modified")
    reviews: list[dict] = Field(default_factory=list, description="The list of reviews")
    reviewed_ids: list[str] = Field(default_factory=list, description="The list of reviewed document ids")


class Review(BaseModel):
    id: int = Field(..., description="The unique identifier for the review")
    user_id: int = Field(..., description="The unique identifier for the user who made the review")
    collection_ids: list[str] = Field(default_factory=list, description="The list of collection ids")
    state: ReviewState = Field(..., description="The current state of the review")
    reviewd_states: list[ReviewState] = Field(default_factory=list, description="The list of past reviewd states")



