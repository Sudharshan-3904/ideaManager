# 🗺️ Idea Manager — Roadmap

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
- [ ] Write basic tests for create, read, update, and delete operations

---

## Phase 3 — Desktop GUI ✅ _(Completed)_

Build the PyQt6 interface, panel by panel.

- [x] Set up `main.py` as the application entry point
- [x] Create `main_window.py` — top-level window with a two-panel layout
- [x] Build `idea_list_panel.py` — scrollable table of all ideas on the left
- [x] Build `idea_detail_panel.py` — full idea view and edit form on the right
- [x] Build `hurdle_panel.py` — sub-panel within the detail view to view and add hurdles
- [x] Wire up signals between panels (e.g. selecting an idea loads its details)

---

## Phase 4 — Core Interactions ✅ _(Mostly Completed)_

Make the app fully usable for daily idea tracking.

- [x] Add new idea via a form dialog
- [x] Edit idea fields inline in the detail panel
- [x] Delete an idea with a confirmation prompt
- [x] Add a new hurdle to any idea
- [ ] Delete a hurdle
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

## Phase 6 — Extensions 🔲 _(In Progress)_

Longer-term ideas to expand the app.

- [x] Minimal Deliverables tracker — section within each idea
- [x] Future Extensions notes section per idea
- [ ] Sort ideas by title, date created, or number of hurdles
- [ ] Keyboard shortcuts for common actions (new idea, save, delete)
- [ ] Empty state UI for when no ideas have been added yet
- [ ] Export ideas to PDF or Markdown
- [ ] Import ideas from a CSV file
- [ ] Tagging and categorization system
