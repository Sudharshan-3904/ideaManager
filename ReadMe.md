# Idea Manager

A PyQt6 desktop application for capturing, organizing, and tracking your project and business ideas — complete with structured metadata, obstacle logging, and target customer profiling.

---

## Overview

Idea Manager is a personal productivity tool designed to help you move ideas from a fleeting thought to a structured, actionable concept. Each idea is broken down into its core components — what it is, who it's for, and what stands in the way — and persisted locally in a CSV file for simplicity and portability.

---

## Features

- **Create & manage ideas** with titles, descriptions, and target customer profiles
- **Track hurdles** — log obstacles as structured entries with a date, a main setback label, and a detailed description
- **Tabular idea browser** — view all your ideas in a clean, formatted table (powered by PrettyTable)
- **CSV-backed persistence** — data is stored in a plain `ideas.csv` file; no database required
- **PyQt6 desktop interface** — a native desktop GUI for comfortable, distraction-free use

---

## Project Structure

```
idea-manager/
├── ideas.csv           # Local data store (auto-created on first run)
├── components.py       # Core data models: Idea and Hurdle classes
├── ideaManager.py      # Main application entry point and UI logic
├── definitions.txt     # Design notes and class planning
└── tester.py           # Development scratch/test script
```

---

## Data Models

### `Idea`

Represents a single project or business idea.

| Field                  | Type           | Description                                 |
| ---------------------- | -------------- | ------------------------------------------- |
| `title`                | `str`          | Short name for the idea                     |
| `description`          | `str`          | Full description of the concept             |
| `hurdles`              | `list[Hurdle]` | List of obstacles associated with this idea |
| `target_customers`     | `str`          | Who this idea serves                        |
| `minimal_deliverables` | _(planned)_    | The smallest shippable version              |
| `future_extensions`    | _(planned)_    | Possible expansions beyond the MVP          |

### `Hurdle`

Represents a single obstacle or challenge tied to an idea.

| Field          | Type       | Description                           |
| -------------- | ---------- | ------------------------------------- |
| `date`         | `datetime` | When the hurdle was identified        |
| `main_setback` | `str`      | A short label for the obstacle        |
| `description`  | `str`      | Detailed explanation of the challenge |

---

## Planned Roadmap

- [ ] Full PyQt6 GUI with idea list, detail panel, and hurdle tracker
- [ ] Add/edit/delete ideas from the interface
- [ ] Log and review hurdles per idea
- [ ] `Minimal Deliverables` and `Future Extensions` fields per idea
- [ ] CSV import/export
- [ ] Sortable/filterable idea table view

---

## Dependencies

```
pandas
prettytable
PyQt6
```

Install with:

```bash
pip install pandas prettytable PyQt6
```

---

## Getting Started

```bash
git clone <repo-url>
cd idea-manager
pip install pandas prettytable PyQt6
python ideaManager.py
```

---

## Notes

This project is in early development. The data models in `components.py` are largely defined; the GUI layer in `ideaManager.py` is the next major area of work.
