# GRAD v2 — project rules

GRAD is a desktop tool for flight-test data: load recordings, derive parameters with formulas,
inspect them on time plots, and compute strain-gauge calibration coefficients by regression.
v1 lives in `legacy/` for reference only: never import from it, never edit it.

## Architecture (details in docs/architecture.md)
- `src/grad/core` is pure Python with no Qt imports. All data logic lives here.
- `src/grad/ui` is PySide6 + pyqtgraph. It calls core and never mutates data directly.
- Raw data is immutable after load. Every change is an operation appended to the project journal;
  working data = pipeline(raw, journal, formulas). Undo = drop the last operation.
- Formulas define new (derived) parameters only, are stored by parameter name, and are evaluated
  by our own AST interpreter with a function whitelist. Never eval/exec user text.
- Project file `.gradproj` = ZIP (stored) with `raw.parquet` + `project.json`
  (schema_version, meta, parameters, formulas, journal, calibrations). CSV is for import/export only.
- Sample rate and time column are project metadata. Never hardcode a sample rate.
- Never round stored or computed values. Round only for display, by significant digits (e.g. `.6g`).

## Conventions
- Python 3.12, uv, type hints everywhere, dataclasses for domain objects.
- Identifiers, docstrings and comments in English. User-facing UI text in Russian, kept in `ui/strings.py`.
- Core raises specific exceptions (subclasses of `GradError`) with messages fit to show the user.
  No `except Exception: return False`.
- Resources via `importlib.resources`, never paths relative to the working directory.

## Workflow
- One phase = one branch `v2/phase-N-<slug>` = one PR. Stay inside the phase scope;
  list anything else under "Follow-ups" in the PR description.
- Every core function gets pytest tests, including edge cases: NaN, empty range, non-uniform time,
  more columns than rows, Cyrillic names, names with dots and spaces.
- Before finishing: `uv run ruff check --fix`, `uv run ruff format`, `uv run pytest` — all green.
- If a change contradicts docs/architecture.md, update that doc first in a separate commit and say why.
