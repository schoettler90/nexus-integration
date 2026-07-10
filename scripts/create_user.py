import sys
import os
import argparse
import getpass

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mongodb import MongoDB
from src.models import User
from src.security import hash_password


def create_user(user_id: str, name: str, email: str, password: str):
    db = MongoDB()
    try:
        # Check if user exists to avoid duplicates or errors if unique constraints exist (though simpler here)
        existing_user = db.get_user(user_id)
        if existing_user:
            print(f"User {user_id} already exists.")
            return

        new_user = User(
            id=user_id,
            name=name,
            email=email,
            password=hash_password(password),
            review_ids=[],
        )
        created_id = db.create_user(new_user)
        print(f"Successfully created user with ID: {created_id}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", default="user_Cvons95")
    parser.add_argument("--name", default="Cvons95")
    parser.add_argument("--email", required=True)
    parser.add_argument("--password", default=None, help="Prompted securely if omitted")
    args = parser.parse_args()
    password = args.password or getpass.getpass("Password: ")
    create_user(args.id, args.name, args.email, password)
