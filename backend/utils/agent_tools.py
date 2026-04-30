import json
from components.idea import Idea
from components.hurdle import Hurdle
from datetime import datetime

class AgentTools:
    def __init__(self, repo):
        self.repo = repo

    def get_tool_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "list_ideas",
                    "description": "Get a list of all existing ideas in the portfolio.",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_idea_details",
                    "description": "Get detailed information about a specific idea by its ID or title.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "idea_id": {"type": "string", "description": "The UUID of the idea."},
                            "title": {"type": "string", "description": "The title of the idea (fallback if ID is unknown)."}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "create_new_idea",
                    "description": "Create a new startup idea in the system.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "Catchy title or name for the idea."},
                            "description": {"type": "string", "description": "Short summary of the idea."},
                            "explanation": {"type": "string", "description": "Detailed explanation of the concept."},
                            "tags": {"type": "array", "items": {"type": "string"}, "description": "List of relevant tags."},
                            "status": {"type": "string", "enum": ["Yet to Start", "Planning", "On Going", "Paused", "Stopped"], "description": "Current progress status."}
                        },
                        "required": ["title", "description"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_existing_idea",
                    "description": "Modify an existing idea's details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "idea_id": {"type": "string", "description": "The UUID of the idea to be updated."},
                            "new_title": {"type": "string", "description": "The new title (if changing)."},
                            "description": {"type": "string", "description": "Updated short summary."},
                            "explanation": {"type": "string", "description": "Updated detailed explanation."},
                            "tags": {"type": "array", "items": {"type": "string"}, "description": "Updated tags."},
                            "status": {"type": "string", "description": "Updated status."}
                        },
                        "required": ["idea_id"]
                    }
                }
            }
        ]

    def execute_tool(self, name, arguments, username):
        if name == "list_ideas":
            ideas = self.repo.get_all_ideas(username=username)
            return [i.to_dict() for i in ideas]
        
        elif name == "get_idea_details":
            idea_id = arguments.get("idea_id")
            title = arguments.get("title")
            ideas = self.repo.get_all_ideas(username=username)
            
            for idea in ideas:
                if idea_id and idea.id == idea_id:
                    return idea.to_dict()
                if title and idea.title.lower() == title.lower():
                    return idea.to_dict()
                    
            return {"error": "Idea not found"}

        elif name == "create_new_idea":
            title = arguments.get("title") or arguments.get("name")
            new_idea = Idea(
                title=title,
                description=arguments.get("description", ""),
                explanation=arguments.get("explanation", ""),
                tags=arguments.get("tags", []),
                status=arguments.get("status", "Yet to Start")
            )
            self.repo.add_idea(new_idea, owner_username=username)
            return {"status": "success", "message": f"Idea '{title}' created successfully.", "id": new_idea.id}

        elif name == "update_existing_idea":
            idea_id = arguments.get("idea_id")
            ideas = self.repo.get_all_ideas(username=username)
            target = None
            for i in ideas:
                if i.id == idea_id:
                    target = i
                    break
            
            if not target:
                return {"error": f"Idea with ID '{idea_id}' not found."}

            updated_idea = Idea(
                id=target.id,
                title=arguments.get("new_title", target.title),
                description=arguments.get("description", target.description),
                explanation=arguments.get("explanation", target.explanation),
                tags=arguments.get("tags", target.tags),
                status=arguments.get("status", target.status),
                hurdles=target.hurdles,
                notes=target.notes,
                architecture=target.architecture,
                is_archived=target.is_archived,
                created_at=target.created_at
            )
            self.repo.update_idea(target.id, updated_idea, username=username)
            return {"status": "success", "message": f"Idea '{target.title}' updated successfully."}
        
        return {"error": f"Tool '{name}' not found."}
