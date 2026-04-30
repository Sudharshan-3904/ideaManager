import os
import sys
import hashlib

# Add the current directory to the system path to allow importing project modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.idea_repository import IdeaRepository
from data.db_handler import DBHandler

def hash_password(password: str) -> str:
    """
    Computes a SHA-256 hash of a password string.
    
    Args:
        password (str): The plain-text password to hash.
        
    Returns:
        str: The hex digest of the hashed password.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def migrate():
    """
    Handles the migration of data from the legacy CSV file to the SQLite database.
    Initializes a default user if one does not already exist.
    """
    print("Initializing migration: CSV to SQLite...")
    
    # Define file paths for the legacy CSV and the new SQLite database
    csv_path = os.path.join(os.path.dirname(__file__), 'ideas.csv')
    db_path = os.path.join(os.path.dirname(__file__), 'ideas.db')
    
    # Initialize repository handlers for both storage types
    repo_csv = IdeaRepository(storage_type="csv", file_path=csv_path)
    db = DBHandler(db_path)
    
    # Step 1: Migrate Ideas and related entities
    try:
        ideas = repo_csv.get_all_ideas()
        print(f"Source records found: {len(ideas)} ideas.")
        
        for idea in ideas:
            print(f"Migrating idea: {idea.title}")
            db.save_idea(idea.to_db_dict())
            
        print("Idea migration completed successfully.")
    except Exception as e:
        print(f"Critical error during idea migration: {e}")

    # Step 2: Ensure a default administrative user exists
    try:
        default_username = "JD"
        default_password = "jd"
        hashed_password = hash_password(default_password)
        
        existing_user = db.fetchone("SELECT * FROM users WHERE username = ?", (default_username,))
        if not existing_user:
            db.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                (default_username, hashed_password)
            )
            print(f"Default user '{default_username}' created.")
        else:
            # Sync password hash to ensure consistency
            db.execute(
                "UPDATE users SET password_hash = ? WHERE username = ?", 
                (hashed_password, default_username)
            )
            print(f"User '{default_username}' updated with fresh credentials.")
            
    except Exception as e:
        print(f"Error during user initialization: {e}")

    print("Data migration process finished.")

if __name__ == "__main__":
    migrate()
