# 📁 Idea Manager — Directory Structure

```
idea-manager/
├── main.py
├── ideas.csv
├── components/
│   ├── __init__.py
│   ├── idea.py
│   └── hurdle.py
├── data/
│   ├── __init__.py
│   ├── csv_handler.py
│   └── idea_repository.py
├── ui/
│   ├── __init__.py
│   ├── main_window.py
│   ├── idea_list_panel.py
│   ├── idea_detail_panel.py
│   └── hurdle_panel.py
└── utils/
    ├── __init__.py
    └── formatters.py
```

---

## File Descriptions

### Root

| File | Description |
|---|---|
| `main.py` | Application entry point. Initializes the PyQt6 app and launches the main window. |
| `ideas.csv` | Local flat-file data store. Holds all persisted idea records across sessions. |

---

### `components/` — Data Models

| File | Description |
|---|---|
| `__init__.py` | Exposes `Idea` and `Hurdle` for easy importing across the project. |
| `idea.py` | Defines the `Idea` class with fields: `title`, `description`, `hurdles`, `target_customers`, `minimal_deliverables`, `future_extensions`. Includes methods to update each field and serialize/deserialize to and from CSV rows. |
| `hurdle.py` | Defines the `Hurdle` class with fields: `date`, `main_setback`, `description`. Includes a `loadFromStr()` method to parse hurdles from a comma-separated string stored in the CSV. |

---

### `data/` — Persistence Layer

| File | Description |
|---|---|
| `__init__.py` | Exposes repository and handler classes. |
| `csv_handler.py` | Low-level CSV read/write operations using `pandas`. Handles file creation, row insertion, row update, and row deletion. |
| `idea_repository.py` | Higher-level data access layer. Translates between raw CSV rows and `Idea`/`Hurdle` objects. Used by the UI layer to load, save, and query ideas without touching the CSV directly. |

---

### `ui/` — PyQt6 Interface

| File | Description |
|---|---|
| `__init__.py` | Exposes UI components. |
| `main_window.py` | The top-level `QMainWindow`. Assembles all panels, manages the app layout, and wires up signals between components. |
| `idea_list_panel.py` | Left-side panel showing a scrollable, filterable list of all ideas using a `QTableWidget` (powered by `PrettyTable` for formatting). Emits a signal when an idea is selected. |
| `idea_detail_panel.py` | Right-side panel showing the full details of the currently selected idea. Allows editing of title, description, target customers, minimal deliverables, and future extensions. |
| `hurdle_panel.py` | Sub-panel within the detail view for viewing and adding hurdles to the current idea. Displays hurdles in a table with date, main setback, and description columns. |

---

### `utils/` — Utilities

| File | Description |
|---|---|
| `__init__.py` | Exposes utility functions. |
| `formatters.py` | Helper functions for formatting data for display — e.g. formatting `datetime` objects, truncating long strings for table previews, and serializing hurdle lists to/from CSV-safe strings. |