from fastmcp import FastMCP
from data.idea_repository import IdeaRepository
from components.idea import Idea
import os

# --- MCP Server Initialization ---
mcp = FastMCP("Idea Manager")

# Define repository with absolute path resolution
DB_DIR = os.path.dirname(os.path.abspath(__file__))
repo = IdeaRepository(file_path=os.path.join(DB_DIR, 'ideas.csv'))

@mcp.tool()
def list_ideas():
    """
    Retrieves a list of all ideas currently stored in the repository.
    """
    ideas = repo.get_all_ideas()
    return [idea.to_dict() for idea in ideas]

@mcp.tool()
def get_idea(title: str):
    """
    Fetches detailed information for a specific idea identified by its title.
    """
    ideas = repo.get_all_ideas()
    for idea in ideas:
        if idea.title.lower() == title.lower():
            return idea.to_dict()
    return {"error": "Idea not found"}

@mcp.tool()
def add_idea(title: str, description: str = "", target_customers: str = "", minimal_deliverables: str = "", future_extensions: str = ""):
    """
    Adds a new idea record to the manager with provided details.
    """
    new_idea = Idea(
        title=title,
        description=description,
        target_customers=target_customers,
        minimal_deliverables=minimal_deliverables,
        future_extensions=future_extensions
    )
    repo.add_idea(new_idea)
    return {"status": "success", "message": f"Idea '{title}' created successfully."}

@mcp.tool()
def update_idea(original_title: str, title: str, description: str = "", target_customers: str = "", minimal_deliverables: str = "", future_extensions: str = ""):
    """
    Updates an existing idea's attributes based on its original title.
    """
    updated_idea = Idea(
        title=title,
        description=description,
        target_customers=target_customers,
        minimal_deliverables=minimal_deliverables,
        future_extensions=future_extensions
    )
    repo.update_idea(original_title, updated_idea)
    return {"status": "success", "message": f"Idea '{original_title}' updated successfully."}

@mcp.tool()
def delete_idea(title: str):
    """
    Permanently removes an idea from the repository by title.
    """
    repo.delete_idea(title)
    return {"status": "success", "message": f"Idea '{title}' deleted."}

if __name__ == "__main__":
    mcp.run()
