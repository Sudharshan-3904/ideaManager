from fastapi import FastAPI, HTTPException, Depends, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import hashlib
from datetime import datetime, timedelta
from jose import JWTError, jwt

from data.idea_repository import IdeaRepository
from components.idea import Idea
from components.hurdle import Hurdle
from utils.ai_handler import AIHandler
import json

# --- Core Application Setup ---

SECRET_KEY = "super-secret-key-for-idea-manager"  # Note: Move to environment variables in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # Standard 24-hour expiration

app = FastAPI(
    title="Idea Manager API",
    description="Backend service for managing startup ideas, hurdles, and AI integrations."
)

# --- Middleware & Integration Initializers ---

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Persistence and External Services
DB_PATH = os.path.join(os.path.dirname(__file__), 'ideas.db')
repo = IdeaRepository(storage_type="db", db_path=DB_PATH)
ai_handler = AIHandler(model="llama3")

# Security Schemes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Security Helpers ---

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Verify user exists in DB
    user = repo.db_handler.fetchone("SELECT * FROM users WHERE username = ?", (username,))
    if user is None:
        raise credentials_exception
    return user

# --- Models ---

class HurdleModel(BaseModel):
    main_setback: str
    description: Optional[str] = ""
    date: Optional[str] = ""
    leads: Optional[List[str]] = []

class IdeaModel(BaseModel):
    title: str
    description: Optional[str] = ""
    explanation: Optional[str] = ""
    hurdles: Optional[List[HurdleModel]] = []
    notes: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    architecture: Optional[Dict[str, Any]] = {"nodes": [], "edges": []}
    is_archived: Optional[bool] = False
    status: Optional[str] = "Yet to Start"

# --- Auth Endpoints ---

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and returns a JWT access token.
    """
    user = repo.db_handler.fetchone("SELECT * FROM users WHERE username = ?", (form_data.username,))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if hash_password(form_data.password) != user['password_hash']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

class RegisterModel(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(form_data: RegisterModel):
    """
    Registers a new user identity in the system.
    """
    # Check for existing identity
    existing = repo.db_handler.fetchone("SELECT id FROM users WHERE username = ?", (form_data.username,))
    if existing:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Enforce minimum complexity
    if len(form_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    # Persist hashed credentials
    password_hash = hash_password(form_data.password)
    repo.db_handler.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (form_data.username, password_hash)
    )
    
    return {"status": "success", "message": "User registered successfully"}

# --- Idea Endpoints ---

@app.patch("/ideas/{title}/archive", response_model=dict)
def archive_idea(title: str, archived: bool, current_user: dict = Depends(get_current_user)):
    # Permission check
    role_row = repo.db_handler.fetchone("SELECT role FROM idea_roles WHERE idea_title = ? AND username = ?", (title, current_user['username']))
    if not role_row or role_row['role'] == 'Viewer':
        raise HTTPException(status_code=403, detail="You do not have permission to archive this idea.")

    repo.archive_idea(title, archived, username=current_user['username'])
    return {"status": "success", "message": f"Idea '{title}' {'archived' if archived else 'unarchived'}."}

@app.delete("/ideas/{title}", response_model=dict)
def delete_idea(title: str, current_user: dict = Depends(get_current_user)):
    # Only Owner can delete
    role_row = repo.db_handler.fetchone("SELECT role FROM idea_roles WHERE idea_title = ? AND username = ?", (title, current_user['username']))
    if not role_row or role_row['role'] != 'Owner':
        raise HTTPException(status_code=403, detail="Only the Owner can delete this idea.")

    repo.delete_idea(title)
    # Log audit
    repo.db_handler.log_audit("ideas", title, "DELETE", current_user['username'])
    return {"status": "success", "message": f"Idea '{title}' deleted."}

# --- Collaboration Endpoints ---

class ShareModel(BaseModel):
    target_username: str
    role: str # Owner, Collaborator, Viewer

@app.post("/ideas/{title}/share", response_model=dict)
def share_idea(title: str, share: ShareModel, current_user: dict = Depends(get_current_user)):
    success, message = repo.share_idea(title, current_user['username'], share.target_username, share.role)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"status": "success", "message": message}

@app.get("/ideas/{title}/activities", response_model=List[dict])
def get_activities(title: str, current_user: dict = Depends(get_current_user)):
    # Check access
    role_row = repo.db_handler.fetchone("SELECT 1 FROM idea_roles WHERE idea_title = ? AND username = ?", (title, current_user['username']))
    if not role_row:
        raise HTTPException(status_code=403, detail="Access denied")
    return repo.get_activities(title)

@app.get("/notifications", response_model=List[dict])
def get_notifications(current_user: dict = Depends(get_current_user)):
    return repo.get_notifications(current_user['username'])

@app.patch("/notifications/{notification_id}/read", response_model=dict)
def mark_notification_read(notification_id: int, current_user: dict = Depends(get_current_user)):
    repo.mark_notification_read(notification_id, current_user['username'])
    return {"status": "success"}

@app.get("/ideas", response_model=List[dict])
def list_ideas(current_user: dict = Depends(get_current_user)):
    """
    Retrieves all ideas accessible to the authenticated user.
    """
    ideas = repo.get_all_ideas(username=current_user['username'])
    return [idea.to_dict() for idea in ideas]

@app.get("/ideas/{title}", response_model=dict)
def get_idea(title: str, current_user: dict = Depends(get_current_user)):
    ideas = repo.get_all_ideas()
    for idea in ideas:
        if idea.title.lower() == title.lower():
            return idea.to_dict()
    raise HTTPException(status_code=404, detail="Idea not found")

@app.post("/ideas", response_model=dict)
def add_idea(idea: IdeaModel, current_user: dict = Depends(get_current_user)):
    # Check for duplicate title
    existing = repo.db_handler.fetchone("SELECT title FROM ideas WHERE title = ?", (idea.title,))
    if existing:
        raise HTTPException(status_code=400, detail=f"An idea with title '{idea.title}' already exists.")

    new_idea = Idea(
        title=idea.title,
        description=idea.description,
        explanation=idea.explanation,
        hurdles=[
            Hurdle(
                main_setback=h.main_setback, 
                description=h.description, 
                leads=h.leads,
                date=datetime.strptime(h.date, '%Y-%m-%d %H:%M:%S') if h.date else None
            ) for h in idea.hurdles
        ] if idea.hurdles else [],
        notes=idea.notes,
        tags=idea.tags,
        architecture=idea.architecture,
        is_archived=idea.is_archived,
        status=idea.status
    )
    repo.add_idea(new_idea, owner_username=current_user['username'])
    return {"status": "success", "message": f"Idea '{idea.title}' created."}

@app.put("/ideas/{original_title}", response_model=dict)
def update_idea(original_title: str, idea: IdeaModel, current_user: dict = Depends(get_current_user)):
    updated_idea = Idea(
        title=idea.title,
        description=idea.description,
        explanation=idea.explanation,
        hurdles=[
            Hurdle(
                main_setback=h.main_setback, 
                description=h.description, 
                leads=h.leads,
                date=datetime.strptime(h.date, '%Y-%m-%d %H:%M:%S') if h.date else None
            ) for h in idea.hurdles
        ] if idea.hurdles else [],
        notes=idea.notes,
        tags=idea.tags,
        architecture=idea.architecture,
        is_archived=idea.is_archived,
        status=idea.status
    )
    # Permission check: Only Owner or Collaborator can update
    role_row = repo.db_handler.fetchone("SELECT role FROM idea_roles WHERE idea_title = ? AND username = ?", (original_title, current_user['username']))
    if not role_row:
        raise HTTPException(status_code=403, detail="You do not have permission to edit this idea.")
    if role_row['role'] == 'Viewer':
        raise HTTPException(status_code=403, detail="Viewers cannot edit ideas.")

    repo.update_idea(original_title, updated_idea, username=current_user['username'])
    return {"status": "success", "message": f"Idea '{original_title}' updated."}

@app.get("/export")
def export_ideas(current_user: dict = Depends(get_current_user)):
    """
    Placeholder for data export functionality.
    """
    return {"status": "info", "message": "SQL migration complete. Use database tools for export for now."}

# --- AI Integration Endpoints ---

@app.post("/ai/summarize", response_model=dict)
def ai_summarize(title: str, description: str, current_user: dict = Depends(get_current_user)):
    summary = ai_handler.summarize_idea(title, description)
    return {"summary": summary}

@app.post("/ai/suggest-hurdles", response_model=List[str])
def ai_suggest_hurdles(title: str, description: str, current_user: dict = Depends(get_current_user)):
    return ai_handler.suggest_hurdles(title, description)

@app.post("/ai/feasibility", response_model=dict)
def ai_feasibility(title: str, description: str, current_user: dict = Depends(get_current_user)):
    return ai_handler.rate_feasibility(title, description)

@app.post("/ai/expand", response_model=dict)
def ai_expand(title: str, description: str, current_user: dict = Depends(get_current_user)):
    return ai_handler.expand_idea(title, description)

@app.post("/ai/tags", response_model=List[str])
def ai_generate_tags(title: str, description: str, current_user: dict = Depends(get_current_user)):
    return ai_handler.generate_tags(title, description)

@app.post("/ai/sync-embeddings", response_model=dict)
def ai_sync_embeddings(current_user: dict = Depends(get_current_user)):
    ideas = repo.get_all_ideas(username=current_user['username'])
    count = 0
    for idea in ideas:
        text = f"{idea.title} {idea.description} {idea.target_customers}"
        embedding = ai_handler.get_embedding(text)
        if embedding:
            repo.save_embedding(idea.title, embedding)
            count += 1
    return {"status": "success", "message": f"Synced {count} embeddings."}

@app.get("/ai/search", response_model=List[dict])
def ai_semantic_search(query: str, current_user: dict = Depends(get_current_user)):
    query_embedding = ai_handler.get_embedding(query)
    if not query_embedding:
        raise HTTPException(status_code=500, detail="Failed to generate embedding for query.")
    
    all_embeddings = repo.get_semantic_search_data()
    results = []
    
    for row in all_embeddings:
        title = row['idea_title']
        embedding = json.loads(row['embedding_json'])
        similarity = ai_handler.cosine_similarity(query_embedding, embedding)
        results.append({"title": title, "similarity": float(similarity)})
        
    # Sort by similarity descending
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:10]

@app.post("/settings/ai-model")
def update_ai_model(model_name: str, current_user: dict = Depends(get_current_user)):
    ai_handler.set_model(model_name)
    return {"status": "success", "message": f"AI model set to {model_name}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
