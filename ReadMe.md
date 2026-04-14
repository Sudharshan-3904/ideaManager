# 💡 IdeaManager — System Modeler & Concept Dashboard

A premium, full-stack application for capturing, organizing, and architecting project and business ideas. Transform fleeting thoughts into structured system blueprints with interactive flowcharting, obstacle tracking, and frictionless data capture.

---

## Key Features

- **Concept Architecture Modeling** — Every idea has its own dedicated system flowchart powered by `@xyflow/react`. Model your logic, data flow, or system architecture directly within each concept.
- **3-Column Mission Control** — A high-density dashboard for analyzing target markets, MVP deliverables, and visionary extensions.
- **Quick-Add Thought Notes** — Log insights as they happen without leaving the main dashboard.
- **Hurdle Tracking** — Define obstacles and potential leads to overcome blockers, with full historical logging.
- **Premium Dark Ecosystem** — A sleek, modern UI with glassmorphism effects, vibrant color-coded states, and smooth micro-animations.
- **CSV persistence** — High-performance data storage using a structured `ideas.csv` localized within the backend.

---

## Technology Stack

| Layer          | Tech                                                                 |
| -------------- | -------------------------------------------------------------------- |
| **Frontend**   | React 19, Vite, Tailwind CSS 4, Lucide Icons                         |
| **Backend**    | FastAPI (Python 3.10+), Uvicorn, Pydantic                            |
| **Diagramming**| XyFlow (@xyflow/react)                                               |
| **Data Layer** | Custom CSV Repository Pattern with JSON serialization for diagrams   |

---

## Project Structure

```bash
ideaManager/
├── backend/                # Python FastAPI Server
│   ├── components/         # Domain Models (Idea, Hurdle)
│   ├── data/               # Repository & CSV Logic
│   ├── main.py             # API Entry Point
│   └── ideas.csv           # Persistent Data Store
├── frontend/               # React Vite Application
│   ├── src/
│   │   ├── components/     # ArchitectureDiagram, Sidebar, etc.
│   │   ├── App.jsx         # Dashboard Logic & UI
│   │   └── api.js          # Axios Configuration
│   └── tailwind.config.js  # Styling System
└── Docs/                   # Legacy & System Documentation
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+

### 2. Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
*Server will start on `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*Access the dashboard via `http://localhost:5173`*

---

## System Details

### `Idea` Object
Every Idea is more than just text. It is a container that holds:
- **Title & Metadata**: Target market and MVP goals.
- **Architecture**: A JSON-serialized representation of your XyFlow diagram.
- **Hurdles**: Historically tracked blockers and resolution leads.
- **Notes**: Chronological thought logs.

### Dashboards & Views
- **Dashboard View**: Side-by-side management of hurdles and notes with Quick-Add support.
- **Architecture View**: Full-screen canvas for modeling system architecture. Changes sync automatically to the backend.

---

## elease Notes
Recent updates included a complete migration from PyQt6 to a decoupled FastAPI/React architecture to support collaborative modeling and multi-view persistence.

---