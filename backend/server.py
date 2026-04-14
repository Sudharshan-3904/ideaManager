from fastmcp import FastMCP
from data.idea_repository import IdeaRepository
from components.idea import Idea
import os

# Initialize FastMCP
mcp = FastMCP("Idea Manager")

# Initialize Repository (relative path fixed for backend folder)
repo = IdeaRepository(os.path.join(os.path.dirname(__file__), 'ideas.csv'))

@mcp.tool()
def list_ideas():
    """List all ideas from the repository."""
    ideas = repo.get_all_ideas()
    return [idea.to_dict() for idea in ideas]

@mcp.tool()
def get_idea(title: str):
    """Get detailed information about a specific idea by title."""
    ideas = repo.get_all_ideas()
    for idea in ideas:
        if idea.title.lower() == title.lower():
            return idea.to_dict()
    return {"error": "Idea not found"}

@mcp.tool()
def add_idea(title: str, description: str = "", target_customers: str = "", minimal_deliverables: str = "", future_extensions: str = ""):
    """Add a new idea to the manager."""
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
    """Update an existing idea."""
    updated_idea = Idea(
        title=title,
        description=description,
        target_customers=target_customers,
        minimal_deliverables=minimal_deliverables,
        future_extensions=future_extensions
    )
    repo.update_idea(original_title, updated_idea)
    return {"status": "success", "message": f"Idea '{original_title}' updated to '{title}'."}

@mcp.tool()
def delete_idea(title: str):
    """Delete an idea by title."""
    repo.delete_idea(title)
    return {"status": "success", "message": f"Idea '{title}' deleted."}

if __name__ == "__main__":
    mcp.run()
