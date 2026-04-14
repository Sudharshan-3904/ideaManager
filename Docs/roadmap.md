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

---

## Phase 8 — Persistence Layer (SQL Migration) ⏳ _(Planned)_

Moving from flat CSV to a robust relational database for atomicity and faster querying.

- [ ] Design SQLite schema for core tables: `Ideas`, `Hurdles`, `Notes`, and `Tags`
- [ ] Implement `backend/data/db_manager.py` — unified interface for all DB interactions
- [ ] Create `migration_csv_to_sqlite.py` script for painless data transition
- [ ] Configure `IdeaRepository` to leverage the SQLite backend instead of CSV

---

## Phase 9 — Identity & Access (Basic Auth) ⏳ _(Planned)_

Securing personal data for solo testing environments.

- [ ] Create `Users` table with username and salted/hashed password storage (`bcrypt`)
- [ ] Implement Backend Login endpoint returning JWT or session tokens
- [ ] Secure all sensitive API endpoints with authentication middleware
- [ ] Add Frontend Login overlay and session persistence with LocalStorage

---

## Phase 10 — Frontend Resilience & UX Polish ⏳ _(Planned)_

Refining the interface for a smoother, professional-grade user experience.

- [ ] Implement global loading states and skeleton loaders for all Dashboard sectors
- [ ] Replace native Browser `alert()` and `confirm()` prompts with themed components
- [ ] Integrate a Toast Notification system for operation feedback (Success/Error)
- [ ] Implement state persistence for Search Query and Filter settings across refreshes

---

## Phase 11 — Logic Validation & Data Integrity ⏳ _(Planned)_

Hardening business rules to prevent data corruption and accidental loss.

- [ ] Implement strict server-side model validation (Unique titles, date adherence)
- [ ] Add "Archival" feature (Soft Delete) with a dedicated "Archived" UI tab
- [ ] Sanitize and normalize all string inputs to avoid breakage
- [ ] Implement an automated DB backup mechanism on data change

