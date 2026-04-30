# 📁 Idea Manager — Directory Structure

```
idea-manager/
├── backend/                # FastAPI Application (Python)
│   ├── main.py             # Main API entry point (FastAPI)
│   ├── server.py           # MCP Server implementation
│   ├── database_migrate.py # SQL migration script
│   ├── ideas.db            # SQLite database (Primary Store)
│   ├── ideas.csv           # Legacy CSV store
│   ├── components/         # Data Models
│   │   ├── hurdle.py       # Hurdle class model
│   │   └── idea.py         # Idea class model
│   ├── data/               # Persistence Layer
│   │   ├── db_handler.py   # SQLite CRUD operations
│   │   ├── csv_handler.py  # CSV read/write operations
│   │   └── idea_repository.py # High-level data abstraction
│   └── utils/              # Helper utilities
│       ├── ai_handler.py   # AI (Ollama/Llama3) integration
│       └── formatters.py   # Data formatting helpers
├── frontend/               # React Application (Vite + JS)
│   ├── src/                # Frontend source code
│   │   ├── main.jsx        # App entry point
│   │   ├── App.jsx         # Main application logic & UI
│   │   ├── api.js          # API client for backend communication
│   │   ├── components/     # UI Components
│   │   │   └── ArchitectureDiagram.jsx # Specialized visual component
│   │   └── assets/         # Static assets
│   ├── index.html          # HTML template
│   ├── package.json        # Frontend dependencies
│   ├── tailwind.config.js  # Styling configuration
│   └── vite.config.js      # Vite build configuration
├── Docs/                   # Documentation
│   └── directoryStructure.md # This file
└── ReadMe.md               # Project overview and setup instructions
```

---

## File Descriptions

### Backend (`backend/`)

| File | Description |
|---|---|
| `main.py` | FastAPI application defining REST endpoints for CRUD operations, AI suggestions, and authentication. |
| `server.py` | MCP (Model Context Protocol) server implementation allowing AI agents to interact with the Idea Manager tools. |
| `ideas.db` | SQLite database storing users, ideas, hurdles, audit logs, and collaboration data. |
| `database_migrate.py` | Script to migrate data from the legacy CSV format to the new SQL database. |

### Backend Components & Data

| Directory/File | Description |
|---|---|
| `components/idea.py` | Defines the `Idea` model including title, description, hurdles, status, and architecture metadata. |
| `components/hurdle.py` | Defines the `Hurdle` model for tracking setbacks and potential solutions. |
| `data/db_handler.py` | Handles direct SQLite interactions, including schema initialization and row-level operations. |
| `data/idea_repository.py` | The central repository pattern implementation that switches between DB and CSV storage. |
| `utils/ai_handler.py` | Interfaces with Ollama (Llama 3) for idea expansion, summarization, and semantic search. |

---

### Frontend (`frontend/`)

| File | Description |
|---|---|
| `src/App.jsx` | The core React component managing application state, routing, and the main dashboard UI. |
| `src/api.js` | Axios-based service for making authenticated requests to the FastAPI backend. |
| `src/main.jsx` | Initializes the React application and mounts it to the DOM. |
| `src/index.css` | Global styles, including Tailwind CSS directives and custom animations. |
| `components/ArchitectureDiagram.jsx` | A specialized component using React Flow (or similar) to visualize idea architectures. |

---

### Documentation (`Docs/`)

| File | Description |
|---|---|
| `directoryStructure.md` | Detailed breakdown of the project's folder organization and file responsibilities. |
| `ReadMe.md` | (Root) Setup guide, feature list, and high-level architectural overview. |

---