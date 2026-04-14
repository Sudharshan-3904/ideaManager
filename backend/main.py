from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from datetime import datetime
from data.idea_repository import IdeaRepository
from components.idea import Idea
from components.hurdle import Hurdle

app = FastAPI(title="Idea Manager API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In development, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Repository
repo = IdeaRepository(os.path.join(os.path.dirname(__file__), 'ideas.csv'))

class HurdleModel(BaseModel):
    main_setback: str
    description: Optional[str] = ""
    date: Optional[str] = ""
    leads: Optional[List[str]] = []

class IdeaModel(BaseModel):
    title: str
    description: Optional[str] = ""
    target_customers: Optional[str] = ""
    minimal_deliverables: Optional[str] = ""
    future_extensions: Optional[str] = ""
    hurdles: Optional[List[HurdleModel]] = []
    notes: Optional[List[str]] = []
    architecture: Optional[Dict[str, Any]] = {"nodes": [], "edges": []}


@app.get("/ideas", response_model=List[dict])
def list_ideas():
    ideas = repo.get_all_ideas()
    return [idea.to_dict() for idea in ideas]

@app.get("/ideas/{title}", response_model=dict)
def get_idea(title: str):
    ideas = repo.get_all_ideas()
    for idea in ideas:
        if idea.title.lower() == title.lower():
            return idea.to_dict()
    raise HTTPException(status_code=404, detail="Idea not found")

@app.post("/ideas", response_model=dict)
def add_idea(idea: IdeaModel):
    new_idea = Idea(
        title=idea.title,
        description=idea.description,
        target_customers=idea.target_customers,
        minimal_deliverables=idea.minimal_deliverables,
        future_extensions=idea.future_extensions,
        hurdles=[
            Hurdle(
                main_setback=h.main_setback, 
                description=h.description, 
                leads=h.leads,
                date=datetime.strptime(h.date, '%Y-%m-%d %H:%M:%S') if h.date else None
            ) for h in idea.hurdles
        ] if idea.hurdles else [],
        notes=idea.notes,
        architecture=idea.architecture
    )
    repo.add_idea(new_idea)
    return {"status": "success", "message": f"Idea '{idea.title}' created."}

@app.put("/ideas/{original_title}", response_model=dict)
def update_idea(original_title: str, idea: IdeaModel):
    updated_idea = Idea(
        title=idea.title,
        description=idea.description,
        target_customers=idea.target_customers,
        minimal_deliverables=idea.minimal_deliverables,
        future_extensions=idea.future_extensions,
        hurdles=[
            Hurdle(
                main_setback=h.main_setback, 
                description=h.description, 
                leads=h.leads,
                date=datetime.strptime(h.date, '%Y-%m-%d %H:%M:%S') if h.date else None
            ) for h in idea.hurdles
        ] if idea.hurdles else [],
        notes=idea.notes,
        architecture=idea.architecture
    )
    repo.update_idea(original_title, updated_idea)
    return {"status": "success", "message": f"Idea '{original_title}' updated."}

@app.delete("/ideas/{title}", response_model=dict)
def delete_idea(title: str):
    repo.delete_idea(title)
    return {"status": "success", "message": f"Idea '{title}' deleted."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
