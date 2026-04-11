from components.idea import Idea
from data.csv_handler import CSVHandler

class IdeaRepository:
    def __init__(self, file_path='ideas.csv'):
        self.handler = CSVHandler(file_path)

    def get_all_ideas(self):
        """Retrieves all ideas from storage as Idea objects."""
        raw_data = self.handler.read_all()
        return [Idea.from_dict(row) for row in raw_data]

    def save_all_ideas(self, ideas):
        """Persists a list of Idea objects to storage."""
        data_list = [idea.to_dict() for idea in ideas]
        self.handler.write_all(data_list)

    def add_idea(self, idea):
        """Adds a single Idea object to storage."""
        self.handler.append_row(idea.to_dict())

    def update_idea(self, original_title, updated_idea):
        """Updates an existing idea by title."""
        ideas = self.get_all_ideas()
        for i, idea in enumerate(ideas):
            if idea.title == original_title:
                ideas[i] = updated_idea
                break
        self.save_all_ideas(ideas)

    def delete_idea(self, title):
        """Deletes an idea by title."""
        ideas = self.get_all_ideas()
        ideas = [idea for idea in ideas if idea.title != title]
        self.save_all_ideas(ideas)
