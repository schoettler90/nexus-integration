"""Migrate plaintext user passwords to bcrypt hashes.

    uv run python scripts/hash_passwords.py

Idempotent: records whose password already looks like a bcrypt hash are
skipped, so re-running is safe.
"""

import os
import sys

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.security import hash_password, is_bcrypt_hash  # noqa: E402


def migrate(users_collection) -> int:
    """Hash every plaintext password in ``users_collection``.

    Returns the number of records migrated (0 on a re-run).
    """
    migrated = 0
    for user in users_collection.find({}):
        password = user.get("password")
        if not password or is_bcrypt_hash(password):
            continue
        users_collection.update_one(
            {"id": user["id"]},
            {"$set": {"password": hash_password(password)}},
        )
        migrated += 1
    return migrated


def main() -> None:
    from src.mongodb import MongoDB

    db = MongoDB()
    try:
        migrated = migrate(db.users_collection)
        print(f"Migrated {migrated} plaintext password(s) to bcrypt.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
