# Idea Manager

A PyQt6 desktop application for capturing, organizing, and tracking your project and business ideas — complete with structured metadata, obstacle logging, and target customer profiling.

---

## Overview

Idea Manager is a personal productivity tool designed to help you move ideas from a fleeting thought to a structured, actionable concept. Each idea is broken down into its core components — what it is, who it's for, and what stands in the way — and persisted locally in a CSV file for simplicity and portability.

---

## Features

- **Create & manage ideas** with titles, descriptions, and target customer profiles
- **Modern Dark UI** — a sleek, professional interface built with PyQt6 and custom QSS styling
- **Track hurdles** — log obstacles as structured entries with a date, a main setback label, and a detailed description
- **Tabular idea browser** — search and filter through all your ideas in a clean, scrollable table
- **CSV-backed persistence** — data is stored in a plain `ideas.csv` file; no database required
- **Desktop interface** — a native desktop application for comfortable, distraction-free use

---

## Project Structure

```
idea-manager/
├── main.py             # Application entry point
├── ideas.csv           # Local data store
├── components/         # Core data models (Idea, Hurdle)
├── data/               # Persistence layer (CSV handling)
├── ui/                 # PyQt6 Interface & Styles
├── utils/              # Helper functions
└── Docs/               # Project documentation
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
| `minimal_deliverables` | `str`          | The smallest shippable version              |
| `future_extensions`    | `str`          | Possible expansions beyond the MVP          |

### `Hurdle`

Represents a single obstacle or challenge tied to an idea.

| Field          | Type       | Description                           |
| -------------- | ---------- | ------------------------------------- |
| `date`         | `datetime` | When the hurdle was identified        |
| `main_setback` | `str`      | A short label for the obstacle        |
| `description`  | `str`      | Detailed explanation of the challenge |

---

- [x] Full PyQt6 GUI with idea list, detail panel, and hurdle tracker
- [x] Modern Dark Mode styling
- [x] Add/edit/delete ideas from the interface
- [x] Log and review hurdles per idea
- [x] `Minimal Deliverables` and `Future Extensions` fields per idea
- [ ] Sortable idea table view
- [ ] CSV import/export

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
python main.py
```

---

## Notes

This project has recently undergone a major UI overhaul to provide a premium dark-themed experience. Core functionality is stable, and future work will focus on export capabilities and enhanced organization tools.
