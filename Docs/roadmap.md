# 🗺️ Idea Manager — Roadmap

---

## Phase 1 — Foundation 🔲 _(Not Started)_

Core data models and local persistence.

- [ ] Define `Idea` class with title, description, hurdles, and target customers
- [ ] Define `Hurdle` class with date, main setback, and description
- [ ] Set up `ideas.csv` as the local data store
- [ ] Fix bugs in `components.py` (variable references, return types)
- [ ] Implement `loadDataFromFile()` fully in `Idea`
- [ ] Implement `loadFromStr()` fully in `Hurdle`
- [ ] Implement `updateFile()` — called after every mutation to persist changes to CSV
- [ ] Add `minimal_deliverables` and `future_extensions` fields to `Idea`

---

## Phase 2 — Data Layer 🔲 _(Not Started)_

Clean separation between data access and business logic.

- [ ] Create `csv_handler.py` for low-level CSV read/write/update/delete via `pandas`
- [ ] Create `idea_repository.py` as a higher-level interface that maps CSV rows ↔ `Idea` objects
- [ ] Replace direct `pd.read_csv` calls in models with repository calls
- [ ] Write basic tests for create, read, update, and delete operations

---

## Phase 3 — Desktop GUI 🔲 _(Not Started)_

Build the PyQt6 interface, panel by panel.

- [ ] Set up `main.py` as the application entry point
- [ ] Create `main_window.py` — top-level window with a two-panel layout
- [ ] Build `idea_list_panel.py` — scrollable table of all ideas on the left
- [ ] Build `idea_detail_panel.py` — full idea view and edit form on the right
- [ ] Build `hurdle_panel.py` — sub-panel within the detail view to view and add hurdles
- [ ] Wire up signals between panels (e.g. selecting an idea loads its details)

---

## Phase 4 — Core Interactions 🔲 _(Not Started)_

Make the app fully usable for daily idea tracking.

- [ ] Add new idea via a form dialog
- [ ] Edit idea fields inline in the detail panel
- [ ] Delete an idea with a confirmation prompt
- [ ] Add a new hurdle to any idea
- [ ] Delete a hurdle
- [ ] Auto-save changes to `ideas.csv` on every edit

---

## Phase 5 — Quality of Life 🔲 _(Not Started)_

Polish and convenience features.

- [ ] Search and filter ideas by title or target customer
- [ ] Sort ideas by title, date created, or number of hurdles
- [ ] Keyboard shortcuts for common actions (new idea, save, delete)
- [ ] Empty state UI for when no ideas have been added yet
- [ ] Validation — prevent saving ideas with empty titles

---

## Phase 6 — Extensions 🔲 _(Future)_

Longer-term ideas to expand the app.

- [ ] Minimal Deliverables tracker — checklist within each idea
- [ ] Future Extensions notes section per idea
- [ ] Export ideas to PDF or Markdown
- [ ] Import ideas from a CSV file
- [ ] Tagging and categorization system
- [ ] Dark mode support
