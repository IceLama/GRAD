# GRAD v2 architecture

## Goals

- Load flight-test recordings (text/CSV now, other formats later) into one project.
- Derive new parameters with formulas and inspect raw and derived parameters on time plots.
- Compute strain-gauge calibration coefficients by single and multiple linear regression.
- Never lose information: raw data stays intact, every change can be undone, results keep full precision.
- Keep the data logic testable without a GUI.

## Layers

| Layer | Package | Rules |
|---|---|---|
| Core | `grad.core` | Pure Python + numpy/pandas/scipy/statsmodels. **No Qt imports.** Owns the data model, loaders, formula interpreter, pipeline, project I/O and regression. Raises `GradError` subclasses with messages fit to show the user. |
| Loaders | `grad.core.loaders` | One module per source format. Each returns raw columns plus detected metadata (encoding, delimiter, time column). |
| UI | `grad.ui` | PySide6 + pyqtgraph. Calls core, renders results, collects user intent. **Never mutates data directly**: it asks core to append an operation. Panels in `ui.panels`, plot widgets in `ui.plots`, user-facing Russian text in `ui/strings.py`. |
| Resources | `grad.resources` | Icons and other assets, loaded with `importlib.resources`. |

Dependencies point one way: `ui -> core`. Core never imports from `ui`, and nothing imports from `legacy/`.

## Data model

A project consists of:

- **Raw data**: the columns as loaded. Immutable after load; stored once.
- **Metadata**: source file info, time column name, sample rate (given or derived from the time column),
  units, and anything else describing the recording. Nothing about the recording is hardcoded.
- **Parameters**: the list of parameter names with per-parameter info (origin raw/derived, unit, display name).
- **Journal**: an ordered list of operations (e.g. rename, delete parameter, time shift, cut range,
  fill gaps). Each operation is a small serialisable record with its arguments, not a data snapshot.
- **Formulas**: a mapping `parameter name -> expression` that defines **derived** parameters only.
  Formulas never overwrite raw parameters. Expressions are parsed into an AST and evaluated by our own
  interpreter with a whitelist of functions; user text is never passed to `eval`/`exec`.
- **Calibrations**: saved regression setups and their results (inputs, range, coefficients, statistics).

## Pipeline

```
raw data ──> apply journal (in order) ──> evaluate formulas (dependency order) ──> working data
```

- Working data is always *computed*: `working = pipeline(raw, journal, formulas)`. It is a cache, never saved.
- **Undo** drops the last journal operation and recomputes the working data.
- Formulas are evaluated in topological order of their references; cycles and unknown names are
  reported as errors naming the parameter, not as silent failures.
- Values are never rounded in storage or computation. Rounding happens only at display time, by
  significant digits (e.g. `.6g`).

## Project file `.gradproj`

A ZIP archive (stored, no compression; parquet is already compressed) containing:

- `raw.parquet`: the raw data exactly as loaded, column names preserved (Cyrillic, dots and spaces allowed).
- `project.json`: `schema_version`, `meta`, `parameters`, `formulas`, `journal`, `calibrations`.

Opening a project reads both entries and runs the pipeline. `schema_version` allows forward migrations.
CSV is used only for import and export, never as the project format.

## What this design removes from v1

| v1 problem | v2 answer |
|---|---|
| Formulas stored inside the data as an extra `__Формулы__` column, row *i* holding the formula of column *i*. Breaks when there are more columns than rows and when columns are reordered or deleted. | Formulas live in `project.json`, keyed by parameter name. |
| Formulas recompute values in place, including over raw parameters; no undo ("НЕ ДОБАВЛЯТЬ ФОРМУЛЫ В ИСХОДНЫЕ ПАРАМЕТРЫ!"). Logical formulas run through `exec`. | Raw data is immutable, formulas only define new parameters, every change is a journal operation, undo is built in. Formulas go through a whitelisted AST interpreter. |
| One global DataFrame (`MainCode.data`) mutated from any window, so windows go out of sync or crash. | Core owns the project; UI requests operations and redraws from working data. |
| Separate conversion step: import CSV, write a `.grad` text file, then open it. | Loaders read source files directly into a project; saving writes `.gradproj`. |
| Sample rate hardcoded to 128 Hz in plot code. | Sample rate and time column are project metadata. |
| Results rounded with `np.round(..., 6)` when formulas are applied. | No rounding of stored or computed values; display-only formatting by significant digits. |
| `except Exception: return False` everywhere, hiding the cause. | Specific `GradError` subclasses with user-readable messages. |

## Later: live telemetry (not designed yet)

A live telemetry source may be added later as another loader that feeds a ring buffer instead of a
fixed raw table. It is out of scope for now; the only constraint today is to keep loaders behind a
common interface so a streaming source can be added without touching formulas or plots.
