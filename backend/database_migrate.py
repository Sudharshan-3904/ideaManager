import os
import sys
import hashlib

# Add the current directory to path so we can import components/data
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.idea_repository import IdeaRepository
from data.db_handler import DBHandler

# Simple hashing for a solo personal tool
def hash_password(password: str) -> str:
    # Use SHA-256 for simplicity as passlib/bcrypt is failing on this environment
    return hashlib.sha256(password.encode()).hexdigest()

def migrate():
    print("Starting migration from CSV to SQLite...")
    
    csv_path = os.path.join(os.path.dirname(__file__), 'ideas.csv')
    db_path = os.path.join(os.path.dirname(__file__), 'ideas.db')
    
    # Initialize Repo for CSV
    repo_csv = IdeaRepository(storage_type="csv", file_path=csv_path)
    
    # Initialize DB Handler
    db = DBHandler(db_path)
    
    # 1. Migrate Ideas
    try:
        ideas = repo_csv.get_all_ideas()
        print(f"Found {len(ideas)} ideas in CSV.")
        
        for idea in ideas:
            print(f"Migrating: {idea.title}")
            db.save_idea(idea.to_db_dict())
            
        print("Idea migration successful.")
    except Exception as e:
        print(f"Error during idea migration: {e}")

    # 2. Create Default User (JD / jd)
    try:
        hashed_password = hash_password("jd")
        
        # Check if user already exists
        existing_user = db.fetchone("SELECT * FROM users WHERE username = ?", ("JD",))
        if not existing_user:
            db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("JD", hashed_password))
            print("Default user 'JD' created.")
        else:
            # Update password just in case it was stuck
            db.execute("UPDATE users SET password_hash = ? WHERE username = ?", (hashed_password, "JD"))
            print("User 'JD' already exists, updated password hash.")
            
    except Exception as e:
        print(f"Error creating default user: {e}")

    print("Migration complete.")

if __name__ == "__main__":
    migrate()
