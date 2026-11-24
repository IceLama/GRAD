# GRAD

Desktop tool for flight-test data: load recordings, derive parameters with formulas, inspect them on
time plots, and compute strain-gauge calibration coefficients by regression.

**Status: v2 in development.** The application is not usable yet; `grad` currently only prints its version.

## Run from source

Requires [uv](https://docs.astral.sh/uv/). uv installs Python 3.12 if it is missing.

```bash
uv sync
```

```bash
uv run grad
```

Run the checks:

```bash
uv run ruff check
```

```bash
uv run pytest
```

## Layout

- `src/grad/core`: data logic, no Qt.
- `src/grad/ui`: PySide6 + pyqtgraph interface.
- `docs/architecture.md`: design of v2.
- `legacy/`: GRAD v1 (PyQt5), kept for reference only, tagged `v1.0`. Its user manual is
  `legacy/README.md`.
