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

class PromptState(BaseModel):
    user_prompt: str = Field(..., description="The user prompt")
    review_columns: dict = Field(default_factory=dict, description="The review columns")

class ReviewState(BaseModel):
    review_id: str = Field(..., description="The unique identifier for the review")
    date_created: int = Field(..., description="The date the review was created in epoch time")
    date_modified: int = Field(..., description="The date the review was last modified")
    prompt_state: PromptState = Field(..., description="The snapshot of the prompt state for this execution")
    reviews: list[dict] = Field(default_factory=list, description="The list of reviews/results")
    reviewed_ids: list[str] = Field(default_factory=list, description="The list of reviewed document ids")

class Review(BaseModel):
    id: str = Field(..., description="The unique identifier for the review")
    user_id: str = Field(..., description="The unique identifier for the user who made the review")
    collection_ids: list[str] = Field(default_factory=list, description="The list of collection ids")
    prompt_state: PromptState = Field(..., description="The current working draft of the prompt state")
    review_states: list[ReviewState] = Field(default_factory=list, description="The list of past executed review states")
