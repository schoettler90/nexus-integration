
import sys
import os
import json

# Add the project root to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mongodb import MongoDB

def verify_user():
    db = MongoDB()
    try:
        user_id = "user_Cvons95"
        user = db.get_user(user_id)
        if user:
            print(f"User found: {user.model_dump_json(indent=2)}")
        else:
            print(f"User {user_id} not found.")
    except Exception as e:
        print(f"Error verifying user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_user()
