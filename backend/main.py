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

# Configuration
SECRET_KEY = "super-secret-key-for-idea-manager" # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 24 hours

app = FastAPI(title="Idea Manager API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Repository with SQL
DB_PATH = os.path.join(os.path.dirname(__file__), 'ideas.db')
repo = IdeaRepository(storage_type="db", db_path=DB_PATH)

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
    target_customers: Optional[str] = ""
    minimal_deliverables: Optional[str] = ""
    future_extensions: Optional[str] = ""
    hurdles: Optional[List[HurdleModel]] = []
    notes: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    architecture: Optional[Dict[str, Any]] = {"nodes": [], "edges": []}
    is_archived: Optional[bool] = False

# --- Auth Endpoints ---

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = repo.db_handler.fetchone("SELECT * FROM users WHERE username = ?", (form_data.username,))
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    if hash_password(form_data.password) != user['password_hash']:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user['username']})
    return {"access_token": access_token, "token_type": "bearer"}

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
        tags=idea.tags,
        architecture=idea.architecture,
        is_archived=idea.is_archived
    )
    repo.add_idea(new_idea, owner_username=current_user['username'])
    return {"status": "success", "message": f"Idea '{idea.title}' created."}

@app.put("/ideas/{original_title}", response_model=dict)
def update_idea(original_title: str, idea: IdeaModel, current_user: dict = Depends(get_current_user)):
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
        tags=idea.tags,
        architecture=idea.architecture,
        is_archived=idea.is_archived
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
    # Note: Exporting the CSV file directly from current working dir
    # If using SQL, we might want to generate a fresh CSV here.
    # For now, we'll just return the SQLite file or a message.
    return {"status": "info", "message": "SQL migration complete. Use database tools for export for now."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
