"""Sprint 3 hardening: bcrypt roundtrip, no password in responses, migration."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from main import app
from scripts.hash_passwords import migrate
from src.models import User
from src.security import hash_password, is_bcrypt_hash, verify_password

client = TestClient(app)


class _FakeDB:
    """Minimal in-memory stand-in for src.mongodb.MongoDB."""

    def __init__(self):
        self.users: dict[str, User] = {}

    def create_user(self, user: User) -> str:
        self.users[user.id] = user
        return user.id

    def get_user(self, user_id):
        return self.users.get(user_id)

    def get_user_by_email(self, email):
        return next((u for u in self.users.values() if u.email == email), None)

    def update_user(self, user_id, user):
        self.users[user_id] = user
        return True

    def list_users(self):
        return list(self.users.values())


class _FakeUsersCollection:
    """Minimal pymongo-collection stand-in for the migration script."""

    def __init__(self, docs):
        self.docs = {doc["id"]: dict(doc) for doc in docs}

    def find(self, query):
        return [dict(doc) for doc in self.docs.values()]

    def update_one(self, filt, update):
        self.docs[filt["id"]].update(update["$set"])


USER_DATA = {
    "id": "u1",
    "name": "Test User",
    "email": "test@example.com",
    "password": "s3cret!",
    "review_ids": [],
}


def test_bcrypt_roundtrip_create_then_login():
    fake = _FakeDB()
    with patch("main.db", fake):
        response = client.post("/users", json=USER_DATA)
        assert response.status_code == 201

        stored = fake.users["u1"].password
        assert is_bcrypt_hash(stored)
        assert stored != USER_DATA["password"]

        ok = client.post(
            "/login", json={"email": "test@example.com", "password": "s3cret!"}
        )
        assert ok.status_code == 200
        assert ok.json()["user_id"] == "u1"

        wrong = client.post(
            "/login", json={"email": "test@example.com", "password": "wrong"}
        )
        assert wrong.status_code == 401


def test_put_hashes_new_plaintext_password_but_not_a_hash():
    fake = _FakeDB()
    with patch("main.db", fake):
        client.post("/users", json=USER_DATA)
        first_hash = fake.users["u1"].password

        # Re-PUT the record as read (already hashed) → hash unchanged.
        client.put("/users/u1", json={**USER_DATA, "password": first_hash})
        assert fake.users["u1"].password == first_hash

        # PUT a new plaintext password → stored hashed.
        client.put("/users/u1", json={**USER_DATA, "password": "new-secret"})
        stored = fake.users["u1"].password
        assert is_bcrypt_hash(stored) and stored != "new-secret"
        assert verify_password("new-secret", stored)


def test_no_password_key_in_any_user_response():
    fake = _FakeDB()
    with patch("main.db", fake):
        client.post("/users", json=USER_DATA)

        single = client.get("/users/u1")
        assert single.status_code == 200
        assert "password" not in single.json()

        listing = client.get("/users")
        assert listing.status_code == 200
        assert listing.json() and all("password" not in u for u in listing.json())


def test_migration_hashes_plaintext_and_is_idempotent():
    collection = _FakeUsersCollection(
        [
            {"id": "u1", "email": "a@x.com", "password": "plain-one"},
            {"id": "u2", "email": "b@x.com", "password": "plain-two"},
            {"id": "u3", "email": "c@x.com", "password": hash_password("prehashed")},
        ]
    )
    pre_hashed = collection.docs["u3"]["password"]

    assert migrate(collection) == 2
    hashes = {uid: doc["password"] for uid, doc in collection.docs.items()}
    assert all(is_bcrypt_hash(h) for h in hashes.values())
    assert verify_password("plain-one", hashes["u1"])
    assert hashes["u3"] == pre_hashed  # already-hashed record untouched

    # Second run migrates nothing and changes nothing.
    assert migrate(collection) == 0
    assert {uid: doc["password"] for uid, doc in collection.docs.items()} == hashes
