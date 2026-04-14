# Idea Manager — Roadmap

---

## Phase 1 — Foundation ✅ _(Completed)_

Core data models and local persistence.

- [x] Define `Idea` class with title, description, hurdles, and target customers
- [x] Define `Hurdle` class with date, main setback, and description
- [x] Set up `ideas.csv` as the local data store
- [x] Fix bugs in `components.py` (variable references, return types)
- [x] Implement `loadDataFromFile()` fully in `Idea` (implemented via `Idea.from_dict`)
- [x] Implement `loadFromStr()` fully in `Hurdle`
- [x] Implement `updateFile()` (implemented via `IdeaRepository.save_all_ideas`)
- [x] Add `minimal_deliverables` and `future_extensions` fields to `Idea`

---

## Phase 2 — Data Layer ✅ _(Completed)_

Clean separation between data access and business logic.

- [x] Create `csv_handler.py` for low-level CSV read/write/update/delete via `pandas`
- [x] Create `idea_repository.py` as a higher-level interface that maps CSV rows ↔ `Idea` objects
- [x] Replace direct `pd.read_csv` calls in models with repository calls
- [x] Write basic tests for create, read, update, and delete operations via FastAPI documentation (Swagger/Docs)

---

## Phase 3 — Transition to Web ✅ _(Completed)_

Building the modern FastAPI + React interface.

- [x] Set up `main.py` as the FastAPI application entry point
- [x] Build `App.jsx` — high-density grid-based dashboard
- [x] Build `ArchitectureDiagram` — interactive system modeling using XYFlow
- [x] Implement Quick-Add logic for frictionless idea capture
- [x] Migrate all PyQt6 logic to the decoupled architecture

---

## Phase 4 — Core Interactions ✅ _(Mostly Completed)_

Make the app fully usable for daily idea tracking.

- [x] Add new idea via a form dialog
- [x] Edit idea fields inline in the detail panel
- [x] Delete an idea with a confirmation prompt
- [x] Add a new hurdle to any idea
- [x] Delete a hurdle (implemented via Edit form and per-hurdle removal)
- [x] Auto-save changes to `ideas.csv` on every edit

---

## Phase 5 — UI & Aesthetics ✅ _(Completed)_

Modernizing the interface with professional styling.

- [x] Modern Dark Mode support via QSS
- [x] Search and filter ideas by title or target customer
- [x] Card-based layout with rounded corners and consistent spacing
- [x] Visual feedback for button states (hover, pressed)
- [x] Validation — prevent saving ideas with empty titles

---

## Phase 6 — Extensions ✅ _(Completed)_

Longer-term ideas to expand the app.

- [x] Minimal Deliverables tracker — section within each idea
- [x] Future Extensions notes section per idea
- [x] Sort ideas by title, date created, or number of hurdles
- [x] Keyboard shortcuts for common actions (Quick-Add Enter support)
- [x] Empty state UI for missing selections and empty repositories
- [x] Export ideas to PDF or Markdown (Implemented CSV Export)
- [x] Import ideas from a JSON/CSV file (Implemented CSV Import)
- [x] Tagging and categorization system
- [x] Splitted backend and frontend architecture

---

## Phase 7 — Visualization & AI Integration ✅ _(Completed)_

Building internal observability and AI readiness.

- [x] FastMCP Integration for AI Agent tool access
- [x] Interactive System Architecture Flowchart (XYFlow)
- [x] Bi-directional communication modeling (Dotted/Solid arrows)
