# IdeaManager — Intelligence-First Concept Dashboard

A premium, full-stack application designed to transform fleeting thoughts into structured, architected, and AI-validated business concept blueprints. Beyond simple note-taking, **IdeaManager** provides a collaborative workspace for modeling system architectures, tracking execution hurdles, and leveraging Local LLMs for deep concept analysis.

---

## Core Pillars

### Integrated Intelligence (AI)
Leverage local inference for privacy-first idea validation.
- **Ollama Integration**: Seamless connection to `llama3` and other local models.
- **Semantic Search**: Find related ideas using vector embeddings (`nomic-embed-text`).
- **AI Synthesis**: Auto-generate summaries, feasibility scores, and technical tags.
- **Automated Roadmap**: Instantly expand ideas into minimal deliverables and future extensions.

### Concept Architecture
Visualize the "How" alongside the "What".
- **XYFlow Integration**: Every idea features a dedicated interactive flowcharting canvas.
- **Logic Modeling**: Define data flows, component relationships, and system dependencies directly in the dashboard.
- **Auto-Sync**: Architecture diagrams are serialized to SQLite and synced in real-time.

### Secure Collaboration
Transition from a solo brainstorm to a shared team workspace.
- **JWT Authentication**: Robust user management with secure password hashing (SHA-256).
- **Role-Based Access**: Assign `Owner`, `Collaborator`, or `Viewer` roles to your concepts.
- **Activity Streams**: Real-time auditing of who edited what and when.
- **In-App Notifications**: Stay updated on shares and collaborative modifications.

### Professional Persistence
Built for reliability and performance.
- **SQLite Engine**: Migrated from flat files to a robust relational database with full atomicity.
- **Audit Logging**: Every mutation is logged for data integrity and version awareness.
- **Archival Flow**: Soft-delete and archive system to keep your dashboard clean without losing history.

---

## Technology Stack

| Layer          | Tech                                                                 |
| -------------- | -------------------------------------------------------------------- |
| **Frontend**   | React 19, Vite, Tailwind CSS 4, Lucide Icons, Sonner (Toasts)        |
| **Backend**    | FastAPI (Python 3.10+), Uvicorn, Jose (JWT), Pydantic                |
| **AI Engine**  | Ollama (Local LLM API), Numpy (Vector Similarity)                    |
| **Diagramming**| XyFlow (@xyflow/react)                                               |
| **Data Layer** | SQLite (Personal Relational Storage), Repository Pattern             |

---

## Project Structure

```bash
ideaManager/
├── backend/                # FastAPI Application
│   ├── components/         # Domain Models (Idea, Hurdle)
│   ├── data/               # SQLite Handlers & Repository Interface
│   ├── utils/              # AI Integration (Ollama) & Formatters
│   ├── ideas.db            # Primary Relational Store
│   └── main.py             # API Entry Point & Middleware
├── frontend/               # React Application
│   ├── src/
│   │   ├── components/     # Architecture Flow, Dashboard Grids, Auth
│   │   ├── App.jsx         # Global State & UI Layout
│   │   └── api.js          # Unified Axios Client
│   └── index.html          # Entry Point
└── Docs/                   # Technical Roadmap & Specs
```

---

## Getting Started

### 1. Prerequisites
- **Python**: 3.10 or higher
- **Node.js**: 18 or higher
- **Ollama**: (Optional, for AI features) Installed and running with `llama3` and `nomic-embed-text`.

### 2. Backend Setup
```bash
cd backend
# Create virtual environment recommendations
python -m venv venv
source venv/bin/activate # windows: .\venv\Scripts\activate

pip install -r requirements.txt
python main.py
```
*The API will be available at `http://localhost:8000`.*
*Run `python database_migrate.py` to initialize the SQLite database if starting fresh.*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Access the dashboard at `http://localhost:5173`.*

---

## Release Notes

**Current Version: v2.0.0 (Collaborative AI Update)**
- Replaced CSV storage with **SQLite Relational Engine**.
- Implemented **JWT Authentication** and multi-user accounts.
- Added **Collaboration Layer** (Idea sharing & permissions).
- Integrated **Ollama AI Handler** for semantic analysis and search.
- Upgraded UI to **Tailwind CSS 4** and **React 19**.

---