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

## Phase 4 — Core Interactions ✅ _(Completed)_

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

## Phase 8 — Persistence Layer (SQL Migration) ✅ _(Completed)_

Moving from flat CSV to a robust relational database for atomicity and faster querying.

- [x] Design SQLite schema for core tables: `Ideas`, `Hurdles`, `Notes`, and `Tags`
- [x] Implement `backend/data/db_manager.py` — unified interface for all DB interactions
- [x] Create `migration_csv_to_sqlite.py` script for painless data transition
- [x] Configure `IdeaRepository` to leverage the SQLite backend instead of CSV

---

## Phase 9 — Identity & Access (Basic Auth) ✅ _(Completed)_

Securing personal data for solo testing environments.

- [x] Create `Users` table with username and salted/hashed password storage
- [x] Implement Backend Login endpoint returning JWT or session tokens
- [x] Secure all sensitive API endpoints with authentication middleware
- [x] Add Frontend Login overlay and session persistence with LocalStorage

---

## Phase 10 — Frontend Resilience & UX Polish ✅ _(Completed)_

Refining the interface for a smoother, professional-grade user experience.

- [x] Implement global loading states and skeleton loaders for all Dashboard sectors
- [x] Replace native Browser `alert()` and `confirm()` prompts with themed components
- [x] Integrate a Toast Notification system for operation feedback (Success/Error)
- [x] Implement state persistence for Search Query and Filter settings across refreshes

---

## Phase 11 — Logic Validation & Data Integrity ✅ _(Completed)_

Hardening business rules to prevent data corruption and accidental loss.

- [x] Implement strict server-side model validation (Unique titles, date adherence)
- [x] Add "Archival" feature (Soft Delete) with a dedicated "Archived" UI tab
- [x] Sanitize and normalize all string inputs to avoid breakage
- [x] Implement an automated DB backup mechanism on data change

---

## Phase 12 — Multi-User & Collaboration ✅ _(Completed)_

Expanding from a solo tool to a shared workspace.

- [x] Scope all ideas, hurdles, and tags to the authenticated user's account
- [x] Add role system — Owner, Collaborator, Viewer per idea
- [x] Implement "Share Idea" flow — invite another registered user by email/username
- [x] Build a real-time activity feed per idea (who edited what and when)
- [x] Add a full audit log table in SQLite — track all mutations with timestamps and actor
- [x] Add in-app notifications for collaboration events (comment, share, status change)

---

## Phase 13 — AI Integration ✅ _(Completed)_

Making the app intelligent and context-aware using local and cloud LLMs.

- [x] Connect to a local Ollama instance for private AI inference
- [x] Auto-generate hurdle suggestions from an idea's title and description
- [x] AI-powered idea summary — condense all fields into a concise 3-sentence pitch
- [x] Feasibility scoring — rate an idea on effort, novelty, and market fit (1–10)
- [x] "Expand Idea" feature — generate minimal deliverables and future extensions automatically
- [x] Semantic search across all ideas using embeddings (e.g., `nomic-embed-text` via Ollama)
- [x] AI-generated tags — auto-tag ideas based on their content
- [x] Add a model selector in Settings to switch between Ollama models

---

## Phase 14 — Mobile & PWA Support 🔲 _(Planned)_

Making the app usable on any device, offline-first.

- [ ] Convert the frontend into a Progressive Web App (PWA) with a `manifest.json`
- [ ] Implement a Service Worker for offline caching of the dashboard
- [ ] Make all UI components fully responsive for mobile screen sizes
- [ ] Add touch-friendly interactions — swipe to archive, long-press for context menu
- [ ] Implement background sync — queue mutations offline, flush when back online
- [ ] Add an "Install App" prompt for mobile and desktop browsers
- [ ] Test and optimize for Core Web Vitals (LCP, CLS, FID)

---

## Phase 15 — Analytics & Insights 🔲 _(Planned)_

Turning raw idea data into actionable personal metrics.

- [ ] Build an "Insights" dashboard page with charts (recharts or Chart.js)
- [ ] Track idea velocity — how many ideas added per week/month
- [ ] Visualize hurdle frequency — which ideas are most blocked
- [ ] Show tag distribution as a donut/pie chart
- [ ] Display a timeline/Gantt view of ideas by creation date and status
- [ ] Export Insights as a PDF or shareable image
- [ ] Add a "Streak" tracker — how many consecutive days with activity
- [ ] Surface "Stale Ideas" — ideas with no edits in the last 30 days
