"""Read and write `.gradproj` project files.

A project file is a ZIP archive without compression (ZIP_STORED) holding two entries:

- `raw.parquet`: the raw data, one float64 column per raw parameter, bit-exact.
- `project.json`: `schema_version` and everything else (meta, parameters, formulas, journal, calibrations).
  Fields this version does not know are kept and written back unchanged.

Saving is atomic: the archive is written to a temporary file next to the target and moved over it with
`os.replace`, so a failed save never damages the existing file.
"""

import contextlib
import json
import os
import secrets
import zipfile
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from typing import IO, Any, NoReturn

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from grad.core.errors import GradFileError, ProjectFileError, ProjectValidationError, UnsupportedVersionError
from grad.core.project import (
    META_KEYS,
    PARAMETER_KEYS,
    RESERVED_KEYS,
    ParameterMeta,
    Project,
    ProjectMeta,
    utc_now,
)

#: Version of the project.json layout written by this module.
SCHEMA_VERSION = 1
FILE_SUFFIX = ".gradproj"
RAW_ENTRY = "raw.parquet"
JSON_ENTRY = "project.json"


# --- saving -----------------------------------------------------------------------------------------


def save(project: Project, path: str | os.PathLike[str]) -> None:
    """Write `project` to `path` atomically, then mark it saved.

    On failure the file at `path`, if any, is left as it was, no temporary file remains, and the project
    stays dirty. Raises `GradFileError` when the file cannot be written.
    """
    target = Path(path)
    saved_at = utc_now()
    document = _document(project, replace(project.meta, modified=saved_at))
    json_bytes = json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False).encode("utf-8")
    table = _raw_to_table(project.raw)

    temp = target.with_name(f".{target.name}.{secrets.token_hex(4)}.tmp")
    try:
        with open(temp, "xb") as file:
            _write_archive(file, json_bytes, table)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temp, target)
    except BaseException as exc:
        _discard(temp)
        if isinstance(exc, OSError | pa.ArrowException):
            raise GradFileError(f"Could not save project to {target}: {_reason(exc)}", target) from exc
        raise
    project.mark_saved(saved_at)


def _document(project: Project, meta: ProjectMeta) -> dict[str, Any]:
    document: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "meta": _meta_to_json(meta),
        "parameters": [_parameter_to_json(p) for p in project.parameters.values()],
        "formulas": dict(project.formulas),
        "journal": list(project.journal),
        "calibrations": list(project.calibrations),
    }
    document.update(project.extra)
    return document


def _meta_to_json(meta: ProjectMeta) -> dict[str, Any]:
    return {
        "title": meta.title,
        "created": meta.created.isoformat(),
        "modified": meta.modified.isoformat(),
        "sample_rate_hz": meta.sample_rate_hz,
        "time_column": meta.time_column,
        "source_files": list(meta.source_files),
        "notes": meta.notes,
        **meta.extra,
    }


def _parameter_to_json(param: ParameterMeta) -> dict[str, Any]:
    return {
        "name": param.name,
        "unit": param.unit,
        "description": param.description,
        "source": param.source.value,
        **param.extra,
    }


def _raw_to_table(raw: pd.DataFrame) -> pa.Table:
    # Build arrays from numpy directly: `from_pandas=False` keeps NaN as a float value with its exact bits,
    # whereas pandas conversion would turn NaN into null and lose the sign and payload.
    arrays = [pa.array(raw[name].to_numpy(), type=pa.float64(), from_pandas=False) for name in raw.columns]
    return pa.Table.from_arrays(arrays, names=list(raw.columns))


def _write_archive(file: IO[bytes], json_bytes: bytes, table: pa.Table) -> None:
    with zipfile.ZipFile(file, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr(JSON_ENTRY, json_bytes)
        with archive.open(RAW_ENTRY, "w", force_zip64=True) as entry:
            pq.write_table(table, entry)


def _discard(path: Path) -> None:
    # Best effort: a failure to remove the temporary file must not hide the error that caused the cleanup.
    with contextlib.suppress(OSError):
        path.unlink(missing_ok=True)


def _reason(exc: BaseException) -> str:
    if isinstance(exc, OSError) and exc.strerror:
        return exc.strerror
    return str(exc) or type(exc).__name__


# --- loading ----------------------------------------------------------------------------------------


def load(path: str | os.PathLike[str]) -> Project:
    """Read a project from `path`. The returned project is not dirty.

    Raises `UnsupportedVersionError` for files from a newer GRAD, `ProjectFileError` for damaged or
    inconsistent files and `GradFileError` when the file cannot be read at all.
    """
    source = Path(path)
    try:
        with zipfile.ZipFile(source, "r") as archive:
            names = set(archive.namelist())
            if JSON_ENTRY not in names:
                _fail(source, f"it has no {JSON_ENTRY}")
            document = _read_document(archive, source)
            _check_version(document, source)
            if RAW_ENTRY not in names:
                _fail(source, f"it has no {RAW_ENTRY}")
            with archive.open(RAW_ENTRY) as entry:
                table = pq.ParquetFile(entry).read()
    except zipfile.BadZipFile as exc:
        message = f"{source.name} is not a GRAD project file (not a ZIP archive)."
        raise ProjectFileError(message, source) from exc
    except pa.ArrowException as exc:
        raise ProjectFileError(f"Project file {source.name} is damaged: {RAW_ENTRY}: {exc}", source) from exc
    except OSError as exc:
        raise GradFileError(f"Could not read {source}: {_reason(exc)}", source) from exc

    raw = _table_to_frame(table, source)
    try:
        return Project(
            raw,
            meta=_meta_from_json(_get(document, "meta", dict, source), source),
            parameters=_parameters_from_json(_get(document, "parameters", list, source), source),
            formulas=_get(document, "formulas", dict, source),
            journal=_get(document, "journal", list, source),
            calibrations=_get(document, "calibrations", list, source),
            extra={k: v for k, v in document.items() if k not in RESERVED_KEYS},
            dirty=False,
        )
    except ProjectValidationError as exc:
        raise ProjectFileError(f"Project file {source.name} is inconsistent: {exc}", source) from exc


def _fail(source: Path, reason: str) -> NoReturn:
    raise ProjectFileError(f"Project file {source.name} is damaged: {reason}.", source)


def _reject_constant(name: str) -> NoReturn:
    raise ValueError(f"{name} is not valid JSON")


def _read_document(archive: zipfile.ZipFile, source: Path) -> dict[str, Any]:
    try:
        document = json.loads(archive.read(JSON_ENTRY).decode("utf-8"), parse_constant=_reject_constant)
    except (UnicodeDecodeError, ValueError) as exc:
        _fail(source, f"{JSON_ENTRY} is not valid UTF-8 JSON ({exc})")
    if not isinstance(document, dict):
        _fail(source, f"{JSON_ENTRY} must hold a JSON object")
    return document


def _check_version(document: dict[str, Any], source: Path) -> None:
    version = document.get("schema_version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        _fail(source, f"schema_version must be a positive integer, got {version!r}")
    if version > SCHEMA_VERSION:
        raise UnsupportedVersionError(source, version, SCHEMA_VERSION)


def _get[T](obj: dict[str, Any], key: str, kind: type[T], source: Path) -> T:
    if key not in obj:
        _fail(source, f"{key!r} is missing")
    value = obj[key]
    if not isinstance(value, kind):
        _fail(source, f"{key!r} must be a JSON {_JSON_TYPE_NAMES[kind]}")
    return value


_JSON_TYPE_NAMES: dict[type, str] = {dict: "object", list: "array", str: "string"}


def _parse_datetime(obj: dict[str, Any], key: str, source: Path) -> datetime:
    text = _get(obj, key, str, source)
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        _fail(source, f"meta.{key} is not an ISO 8601 date and time: {text!r}")


def _meta_from_json(obj: dict[str, Any], source: Path) -> ProjectMeta:
    defaults = ProjectMeta()
    return ProjectMeta(
        title=obj.get("title", defaults.title),
        created=_parse_datetime(obj, "created", source),
        modified=_parse_datetime(obj, "modified", source),
        sample_rate_hz=obj.get("sample_rate_hz"),
        time_column=obj.get("time_column"),
        source_files=tuple(_get(obj, "source_files", list, source)) if "source_files" in obj else (),
        notes=obj.get("notes", defaults.notes),
        extra={k: v for k, v in obj.items() if k not in META_KEYS},
    )


def _parameters_from_json(entries: list[Any], source: Path) -> dict[str, ParameterMeta]:
    parameters: dict[str, ParameterMeta] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            _fail(source, "every entry of 'parameters' must be a JSON object")
        param = ParameterMeta(
            name=entry.get("name", ""),
            unit=entry.get("unit", ""),
            description=entry.get("description", ""),
            source=entry.get("source", "raw"),
            extra={k: v for k, v in entry.items() if k not in PARAMETER_KEYS},
        )
        if param.name in parameters:
            _fail(source, f"parameter {param.name!r} is listed twice")
        parameters[param.name] = param
    return parameters


def _table_to_frame(table: pa.Table, source: Path) -> pd.DataFrame:
    names = table.column_names
    if len(set(names)) != len(names):
        _fail(source, f"{RAW_ENTRY} has repeated column names")
    for column_field in table.schema:
        if column_field.type != pa.float64():
            _fail(source, f"column {column_field.name!r} in {RAW_ENTRY} is {column_field.type}, not float64")
    if table.num_columns == 0:
        return pd.DataFrame(index=pd.RangeIndex(0))
    # Nulls cannot come from `save`; if a foreign writer produced them they become NaN.
    return table.to_pandas(split_blocks=True)
