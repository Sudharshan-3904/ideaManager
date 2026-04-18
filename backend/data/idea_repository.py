from components.idea import Idea
from data.csv_handler import CSVHandler
from data.db_handler import DBHandler

class IdeaRepository:
    def __init__(self, storage_type="db", file_path='ideas.csv', db_path='ideas.db'):
        self.csv_handler = CSVHandler(file_path)
        self.db_handler = DBHandler(db_path)
        self.storage_type = storage_type

    def get_all_ideas(self, username=None):
        """Retrieves all ideas from storage as Idea objects, optionally scoped to a user."""
        if self.storage_type == "csv":
            raw_data = self.csv_handler.read_all()
            return [Idea.from_dict(row) for row in raw_data]
        elif self.storage_type == "db":
            raw_data = self.db_handler.read_all_ideas(username=username)
            return [Idea.from_db_row(row) for row in raw_data]

    def save_all_ideas(self, ideas):
        """Persists a list of Idea objects to storage. Note: SQL uses atomic saves."""
        if self.storage_type == "csv":
            data_list = [idea.to_csv_dict() for idea in ideas]
            self.csv_handler.write_all(data_list)
        elif self.storage_type == "db":
            for idea in ideas:
                self.db_handler.save_idea(idea.to_db_dict())

    def add_idea(self, idea, owner_username=None):
        """Adds a single Idea object to storage."""
        if self.storage_type == "csv":
            self.csv_handler.append_row(idea.to_csv_dict())
        elif self.storage_type == "db":
            idea_dict = idea.to_db_dict()
            if owner_username:
                idea_dict['owner_username'] = owner_username
            self.db_handler.save_idea(idea_dict)
            if owner_username:
                self.db_handler.log_activity(idea.title, owner_username, "Created", "Idea created")
                self.db_handler.log_audit("ideas", idea.title, "INSERT", owner_username)

    def update_idea(self, original_title, updated_idea, username=None):
        """Updates an existing idea by title."""
        if self.storage_type == "csv":
            ideas = self.get_all_ideas()
            for i, idea in enumerate(ideas):
                if idea.title.strip().lower() == original_title.strip().lower():
                    ideas[i] = updated_idea
                    break
            self.save_all_ideas(ideas)
        elif self.storage_type == "db":
            # If title changed, delete original and save updated
            if original_title.strip().lower() != updated_idea.title.strip().lower():
                self.db_handler.delete_idea(original_title)
            
            idea_dict = updated_idea.to_db_dict()
            if username:
                idea_dict['owner_username'] = username # Keep role consistency if updated by owner
            
            self.db_handler.save_idea(idea_dict)
            
            if username:
                self.db_handler.log_activity(updated_idea.title, username, "Updated", f"Idea updated (Original: {original_title})")
                self.db_handler.log_audit("ideas", updated_idea.title, "UPDATE", username)

    def delete_idea(self, title):
        """Deletes an idea by title."""
        if self.storage_type == "csv":
            ideas = self.get_all_ideas()
            ideas = [idea for idea in ideas if idea.title.strip().lower() != title.strip().lower()]
            self.save_all_ideas(ideas)
        elif self.storage_type == "db":
            self.db_handler.delete_idea(title)
            
    def archive_idea(self, title, status=True, username=None):
        """Archives or unarchives an idea by title."""
        if self.storage_type == "db":
            self.db_handler.execute("UPDATE ideas SET is_archived = ? WHERE title = ?", (1 if status else 0, title))
            if username:
                action = "Archived" if status else "Unarchived"
                self.db_handler.log_activity(title, username, action)
                self.db_handler.log_audit("ideas", title, "PATCH", username, f"is_archived={status}")
        else:
            # Fallback for CSV (less efficient but maintains existing pattern)
            ideas = self.get_all_ideas()
            for idea in ideas:
                if idea.title.strip().lower() == title.strip().lower():
                    idea.is_archived = status
                    break
            self.save_all_ideas(ideas)

    def share_idea(self, title, owner, target, role):
        return self.db_handler.share_idea(title, owner, target, role)

    def get_activities(self, title):
        return self.db_handler.get_activities(title)

    def get_notifications(self, username):
        return self.db_handler.get_notifications(username)

    def mark_notification_read(self, id, username):
        self.db_handler.mark_notification_read(id, username)
