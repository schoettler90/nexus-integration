import os
from typing import Optional, List
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from dotenv import load_dotenv
from src.models import User, Collection as CollectionModel, ReviewState, Review

load_dotenv()

MONGODB_ATLAS_CLUSTER_URI = os.getenv("MONGODB_ATLAS_CLUSTER_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


class MongoDB:
    def __init__(self, database_name: str = DATABASE_NAME):
        """Initialize MongoDB connection."""
        self.client: MongoClient = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
        self.db: Database = self.client[database_name]

        # Collections
        self.users_collection: Collection = self.db["users"]
        self.collections_collection: Collection = self.db["collections"]
        self.reviews_collection: Collection = self.db["reviews"]
        self.review_states_collection: Collection = self.db["review_states"]

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()

    # ==================== User CRUD Operations ====================

    def create_user(self, user: User) -> str:
        """
        Create a new user in the database.

        Args:
            user: User object to create

        Returns:
            str: The ID of the created user
        """
        user_dict = user.model_dump()
        result = self.users_collection.insert_one(user_dict)
        return str(result.inserted_id)

    def get_user(self, user_id: str) -> Optional[User]:
        """
        Get a user by ID.

        Args:
            user_id: The unique identifier for the user

        Returns:
            User object if found, None otherwise
        """
        user_dict = self.users_collection.find_one({"id": user_id})
        if user_dict:
            user_dict.pop("_id", None)  # Remove MongoDB's internal _id
            return User(**user_dict)
        return None

    def update_user(self, user_id: str, user: User) -> bool:
        """
        Update an existing user.

        Args:
            user_id: The unique identifier for the user
            user: Updated User object

        Returns:
            bool: True if user was updated, False otherwise
        """
        user_dict = user.model_dump()
        result = self.users_collection.update_one(
            {"id": user_id},
            {"$set": user_dict}
        )
        return result.modified_count > 0

    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: The unique identifier for the user

        Returns:
            bool: True if user was deleted, False otherwise
        """
        result = self.users_collection.delete_one({"id": user_id})
        return result.deleted_count > 0

    def list_users(self) -> List[User]:
        """
        Get all users from the database.

        Returns:
            List of User objects
        """
        users = []
        for user_dict in self.users_collection.find():
            user_dict.pop("_id", None)
            users.append(User(**user_dict))
        return users

    # ==================== Collection CRUD Operations ====================

    def create_collection(self, collection: CollectionModel) -> str:
        """
        Create a new collection in the database.

        Args:
            collection: Collection object to create

        Returns:
            str: The ID of the created collection
        """
        collection_dict = collection.model_dump()
        result = self.collections_collection.insert_one(collection_dict)
        return str(result.inserted_id)

    def get_collection(self, collection_id: str) -> Optional[CollectionModel]:
        """
        Get a collection by ID.

        Args:
            collection_id: The unique identifier for the collection

        Returns:
            Collection object if found, None otherwise
        """
        collection_dict = self.collections_collection.find_one({"id": collection_id})
        if collection_dict:
            collection_dict.pop("_id", None)
            return CollectionModel(**collection_dict)
        return None

    def update_collection(self, collection_id: str, collection: CollectionModel) -> bool:
        """
        Update an existing collection.

        Args:
            collection_id: The unique identifier for the collection
            collection: Updated Collection object

        Returns:
            bool: True if collection was updated, False otherwise
        """
        collection_dict = collection.model_dump()
        result = self.collections_collection.update_one(
            {"id": collection_id},
            {"$set": collection_dict}
        )
        return result.modified_count > 0

    def delete_collection(self, collection_id: str) -> bool:
        """
        Delete a collection by ID.

        Args:
            collection_id: The unique identifier for the collection

        Returns:
            bool: True if collection was deleted, False otherwise
        """
        result = self.collections_collection.delete_one({"id": collection_id})
        return result.deleted_count > 0

    def list_collections(self) -> List[CollectionModel]:
        """
        Get all collections from the database.

        Returns:
            List of Collection objects
        """
        collections = []
        for collection_dict in self.collections_collection.find():
            collection_dict.pop("_id", None)
            collections.append(CollectionModel(**collection_dict))
        return collections

    def add_document_to_collection(self, collection_id: str, document_id: str) -> bool:
        """
        Add a document ID to a collection's document_ids list.

        Args:
            collection_id: The unique identifier for the collection
            document_id: The document ID to add

        Returns:
            bool: True if document was added, False otherwise
        """
        result = self.collections_collection.update_one(
            {"id": collection_id},
            {"$addToSet": {"document_ids": document_id}}
        )
        return result.modified_count > 0

    def remove_document_from_collection(self, collection_id: str, document_id: str) -> bool:
        """
        Remove a document ID from a collection's document_ids list.

        Args:
            collection_id: The unique identifier for the collection
            document_id: The document ID to remove

        Returns:
            bool: True if document was removed, False otherwise
        """
        result = self.collections_collection.update_one(
            {"id": collection_id},
            {"$pull": {"document_ids": document_id}}
        )
        return result.modified_count > 0

    # ==================== ReviewState CRUD Operations ====================

    def create_review_state(self, review_state: ReviewState) -> str:
        """
        Create a new review state in the database.

        Args:
            review_state: ReviewState object to create

        Returns:
            str: The ID of the created review state
        """
        review_state_dict = review_state.model_dump()
        result = self.review_states_collection.insert_one(review_state_dict)
        return str(result.inserted_id)

    def get_review_state(self, review_id: str) -> Optional[ReviewState]:
        """
        Get a review state by review ID.

        Args:
            review_id: The unique identifier for the review

        Returns:
            ReviewState object if found, None otherwise
        """
        review_state_dict = self.review_states_collection.find_one({"review_id": review_id})
        if review_state_dict:
            review_state_dict.pop("_id", None)
            return ReviewState(**review_state_dict)
        return None

    def update_review_state(self, review_id: str, review_state: ReviewState) -> bool:
        """
        Update an existing review state.

        Args:
            review_id: The unique identifier for the review
            review_state: Updated ReviewState object

        Returns:
            bool: True if review state was updated, False otherwise
        """
        review_state_dict = review_state.model_dump()
        result = self.review_states_collection.update_one(
            {"review_id": review_id},
            {"$set": review_state_dict}
        )
        return result.modified_count > 0

    def delete_review_state(self, review_id: str) -> bool:
        """
        Delete a review state by review ID.

        Args:
            review_id: The unique identifier for the review

        Returns:
            bool: True if review state was deleted, False otherwise
        """
        result = self.review_states_collection.delete_one({"review_id": review_id})
        return result.deleted_count > 0

    def list_review_states(self) -> List[ReviewState]:
        """
        Get all review states from the database.

        Returns:
            List of ReviewState objects
        """
        review_states = []
        for review_state_dict in self.review_states_collection.find():
            review_state_dict.pop("_id", None)
            review_states.append(ReviewState(**review_state_dict))
        return review_states

    # ==================== Review CRUD Operations ====================

    def create_review(self, review: Review) -> str:
        """
        Create a new review in the database.

        Args:
            review: Review object to create

        Returns:
            str: The ID of the created review
        """
        review_dict = review.model_dump()
        result = self.reviews_collection.insert_one(review_dict)
        return str(result.inserted_id)

    def get_review(self, review_id: int) -> Optional[Review]:
        """
        Get a review by ID.

        Args:
            review_id: The unique identifier for the review

        Returns:
            Review object if found, None otherwise
        """
        review_dict = self.reviews_collection.find_one({"id": review_id})
        if review_dict:
            review_dict.pop("_id", None)
            return Review(**review_dict)
        return None

    def update_review(self, review_id: int, review: Review) -> bool:
        """
        Update an existing review.

        Args:
            review_id: The unique identifier for the review
            review: Updated Review object

        Returns:
            bool: True if review was updated, False otherwise
        """
        review_dict = review.model_dump()
        result = self.reviews_collection.update_one(
            {"id": review_id},
            {"$set": review_dict}
        )
        return result.modified_count > 0

    def delete_review(self, review_id: int) -> bool:
        """
        Delete a review by ID.

        Args:
            review_id: The unique identifier for the review

        Returns:
            bool: True if review was deleted, False otherwise
        """
        result = self.reviews_collection.delete_one({"id": review_id})
        return result.deleted_count > 0

    def list_reviews(self) -> List[Review]:
        """
        Get all reviews from the database.

        Returns:
            List of Review objects
        """
        reviews = []
        for review_dict in self.reviews_collection.find():
            review_dict.pop("_id", None)
            reviews.append(Review(**review_dict))
        return reviews

    def get_reviews_by_user(self, user_id: int) -> List[Review]:
        """
        Get all reviews for a specific user.

        Args:
            user_id: The unique identifier for the user

        Returns:
            List of Review objects for the user
        """
        reviews = []
        for review_dict in self.reviews_collection.find({"user_id": user_id}):
            review_dict.pop("_id", None)
            reviews.append(Review(**review_dict))
        return reviews

    def add_collection_to_review(self, review_id: int, collection_id: str) -> bool:
        """
        Add a collection ID to a review's collection_ids list.

        Args:
            review_id: The unique identifier for the review
            collection_id: The collection ID to add

        Returns:
            bool: True if collection was added, False otherwise
        """
        result = self.reviews_collection.update_one(
            {"id": review_id},
            {"$addToSet": {"collection_ids": collection_id}}
        )
        return result.modified_count > 0

    def remove_collection_from_review(self, review_id: int, collection_id: str) -> bool:
        """
        Remove a collection ID from a review's collection_ids list.

        Args:
            review_id: The unique identifier for the review
            collection_id: The collection ID to remove

        Returns:
            bool: True if collection was removed, False otherwise
        """
        result = self.reviews_collection.update_one(
            {"id": review_id},
            {"$pull": {"collection_ids": collection_id}}
        )
        return result.modified_count > 0

    def add_review_state_to_review(self, review_id: int, review_state: ReviewState) -> bool:
        """
        Add a review state to a review's review_states list.

        Args:
            review_id: The unique identifier for the review
            review_state: The ReviewState object to add

        Returns:
            bool: True if review state was added, False otherwise
        """
        review_state_dict = review_state.model_dump()
        result = self.reviews_collection.update_one(
            {"id": review_id},
            {"$push": {"review_states": review_state_dict}}
        )
        return result.modified_count > 0
