
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mongodb import MongoDB
from src.models import User

def create_user():
    db = MongoDB()
    try:
        user_id = "user_Cvons95"
        # Check if user exists to avoid duplicates or errors if unique constraints exist (though simpler here)
        existing_user = db.get_user(user_id)
        if existing_user:
            print(f"User {user_id} already exists.")
            return

        new_user = User(
            id=user_id,
            name="Cvons95",
            review_ids=[]
        )
        created_id = db.create_user(new_user)
        print(f"Successfully created user with ID: {created_id}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user()
