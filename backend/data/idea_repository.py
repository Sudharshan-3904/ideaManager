from components.idea import Idea
from data.csv_handler import CSVHandler
from data.db_handler import DBHandler

class IdeaRepository:
    def __init__(self, storage_type="db", file_path='ideas.csv', db_path='ideas.db'):
        self.csv_handler = CSVHandler(file_path)
        self.db_handler = DBHandler(db_path)
        self.storage_type = storage_type

    def get_all_ideas(self):
        """Retrieves all ideas from storage as Idea objects."""
        if self.storage_type == "csv":
            raw_data = self.csv_handler.read_all()
            return [Idea.from_dict(row) for row in raw_data]
        elif self.storage_type == "db":
            raw_data = self.db_handler.read_all_ideas()
            return [Idea.from_db_row(row) for row in raw_data]

    def save_all_ideas(self, ideas):
        """Persists a list of Idea objects to storage. Note: SQL uses atomic saves."""
        if self.storage_type == "csv":
            data_list = [idea.to_csv_dict() for idea in ideas]
            self.csv_handler.write_all(data_list)
        elif self.storage_type == "db":
            for idea in ideas:
                self.db_handler.save_idea(idea.to_db_dict())

    def add_idea(self, idea):
        """Adds a single Idea object to storage."""
        if self.storage_type == "csv":
            self.csv_handler.append_row(idea.to_csv_dict())
        elif self.storage_type == "db":
            self.db_handler.save_idea(idea.to_db_dict())

    def update_idea(self, original_title, updated_idea):
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
            self.db_handler.save_idea(updated_idea.to_db_dict())

    def delete_idea(self, title):
        """Deletes an idea by title."""
        if self.storage_type == "csv":
            ideas = self.get_all_ideas()
            ideas = [idea for idea in ideas if idea.title.strip().lower() != title.strip().lower()]
            self.save_all_ideas(ideas)
        elif self.storage_type == "db":
            self.db_handler.delete_idea(title)
            
    def archive_idea(self, title, status=True):
        """Archives or unarchives an idea by title."""
        if self.storage_type == "db":
            self.db_handler.execute("UPDATE ideas SET is_archived = ? WHERE title = ?", (1 if status else 0, title))
        else:
            # Fallback for CSV (less efficient but maintains existing pattern)
            ideas = self.get_all_ideas()
            for idea in ideas:
                if idea.title.strip().lower() == title.strip().lower():
                    idea.is_archived = status
                    break
            self.save_all_ideas(ideas)
