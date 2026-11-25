"""Project model: immutable raw data plus metadata, parameters, formulas, journal and calibrations.

Raw data is stored once and never mutated; `Project.raw` hands out copy-on-write views. Metadata objects are
frozen, so every change goes through a `Project` method that marks the project dirty and notifies observers.
"""

import copy
import math
from collections import Counter
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

import numpy as np
import pandas as pd

from grad.core.errors import ProjectValidationError, TimeBaseError


def utc_now() -> datetime:
    """Current time as a timezone-aware UTC datetime."""
    return datetime.now(UTC)


def _check_aware(value: datetime, what: str) -> None:
    if not isinstance(value, datetime):
        raise ProjectValidationError(f"{what} must be a datetime, got {value!r}.")
    if value.tzinfo is None or value.utcoffset() is None:
        raise ProjectValidationError(f"{what} must include a time zone, got {value.isoformat()}.")


def _frozen_extra(extra: Mapping[str, Any], known: frozenset[str], owner: str) -> Mapping[str, Any]:
    """Deep-copy unknown JSON fields so later edits to the source cannot reach the project.

    `known` are the keys the owner writes itself; an extra field with such a key would shadow it on save.
    """
    clash = sorted(known & extra.keys())
    if clash:
        raise ProjectValidationError(f"{owner}: extra fields use reserved keys: {', '.join(clash)}.")
    return MappingProxyType(copy.deepcopy(dict(extra)))


#: Keys of a parameter entry and of `meta` in project.json that the dataclasses below own.
PARAMETER_KEYS: frozenset[str] = frozenset({"name", "unit", "description", "source"})
META_KEYS: frozenset[str] = frozenset(
    {"title", "created", "modified", "sample_rate_hz", "time_column", "source_files", "notes"}
)


class ParameterSource(StrEnum):
    """Where a parameter's values come from."""

    RAW = "raw"
    """A column of the raw data, as loaded."""
    DERIVED = "derived"
    """Computed by a formula."""


@dataclass(frozen=True, slots=True)
class ParameterMeta:
    """Descriptive information about one parameter. Values live in the raw data or come from a formula."""

    name: str
    unit: str = ""
    description: str = ""
    source: ParameterSource = ParameterSource.RAW
    extra: Mapping[str, Any] = field(default_factory=dict, hash=False)
    """Fields of this parameter's entry in project.json that this GRAD does not know; kept for round trips."""

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ProjectValidationError(f"Parameter name must be a non-empty string, got {self.name!r}.")
        for attr in ("unit", "description"):
            if not isinstance(getattr(self, attr), str):
                raise ProjectValidationError(f"Parameter {self.name!r}: {attr} must be a string.")
        try:
            source = ParameterSource(self.source)
        except ValueError:
            raise ProjectValidationError(
                f"Parameter {self.name!r}: unknown source {self.source!r}; "
                f"expected one of {[s.value for s in ParameterSource]}."
            ) from None
        object.__setattr__(self, "source", source)
        object.__setattr__(
            self, "extra", _frozen_extra(self.extra, PARAMETER_KEYS, f"Parameter {self.name!r}")
        )


@dataclass(frozen=True, slots=True)
class ProjectMeta:
    """Information about the recording and the project as a whole."""

    title: str = ""
    created: datetime = field(default_factory=utc_now)
    modified: datetime = field(default_factory=utc_now)
    sample_rate_hz: float | None = None
    """Samples per second, if known. Used to build time when there is no time column."""
    time_column: str | None = None
    """Name of the raw column holding time, if any."""
    source_files: tuple[str, ...] = ()
    notes: str = ""
    extra: Mapping[str, Any] = field(default_factory=dict, hash=False)
    """Fields of `meta` in project.json that this GRAD does not know; kept for round trips."""

    def __post_init__(self) -> None:
        for attr in ("title", "notes"):
            if not isinstance(getattr(self, attr), str):
                raise ProjectValidationError(f"Project {attr} must be a string.")
        _check_aware(self.created, "Creation time")
        _check_aware(self.modified, "Modification time")

        rate = self.sample_rate_hz
        if rate is not None:
            if isinstance(rate, bool) or not isinstance(rate, int | float):
                raise ProjectValidationError(f"Sample rate must be a number, got {rate!r}.")
            rate = float(rate)
            if not (math.isfinite(rate) and rate > 0):
                raise ProjectValidationError(f"Sample rate must be a positive finite number, got {rate!r}.")
            object.__setattr__(self, "sample_rate_hz", rate)

        if self.time_column is not None and (not isinstance(self.time_column, str) or not self.time_column):
            raise ProjectValidationError(f"Time column must be a non-empty string, got {self.time_column!r}.")

        if isinstance(self.source_files, str) or not all(isinstance(f, str) for f in self.source_files):
            raise ProjectValidationError("Source files must be a sequence of strings.")
        object.__setattr__(self, "source_files", tuple(self.source_files))
        object.__setattr__(self, "extra", _frozen_extra(self.extra, META_KEYS, "Project metadata"))


class ProjectChange(StrEnum):
    """What changed; passed to project observers."""

    META = "meta"
    PARAMETERS = "parameters"
    SAVED = "saved"
    """The project was saved: `modified` was updated and the dirty flag cleared."""


ProjectObserver = Callable[[ProjectChange], None]

#: Top-level project.json keys owned by the file format; `Project.extra` must not use them.
RESERVED_KEYS: frozenset[str] = frozenset(
    {"schema_version", "meta", "parameters", "formulas", "journal", "calibrations"}
)


def _validate_raw(raw: pd.DataFrame) -> None:
    if not isinstance(raw, pd.DataFrame):
        raise ProjectValidationError(f"Raw data must be a pandas DataFrame, got {type(raw).__name__}.")
    names = list(raw.columns)
    for name in names:
        if not isinstance(name, str) or not name:
            raise ProjectValidationError(f"Parameter names must be non-empty strings, got {name!r}.")
    duplicates = sorted(name for name, count in Counter(names).items() if count > 1)
    if duplicates:
        raise ProjectValidationError(f"Parameter names must be unique; repeated: {', '.join(duplicates)}.")
    for name, dtype in raw.dtypes.items():
        if dtype != np.dtype(np.float64):
            raise ProjectValidationError(
                f"Parameter {name!r} has type {dtype}; raw data must be float64. "
                "Convert it explicitly before creating the project."
            )
    if not raw.index.equals(pd.RangeIndex(len(raw))):
        raise ProjectValidationError(
            "Raw data must have a default 0..n-1 row index; move time or other index values into a column."
        )
    if not names and len(raw) > 0:
        raise ProjectValidationError("Raw data has rows but no columns.")


class Project:
    """A GRAD project.

    Holds the raw data (never mutated), metadata, per-parameter info, formulas, the operation journal and
    calibrations. Formulas, journal and calibrations are only stored and round-tripped in this version.
    """

    def __init__(
        self,
        raw: pd.DataFrame,
        meta: ProjectMeta | None = None,
        parameters: Mapping[str, ParameterMeta] | None = None,
        formulas: Mapping[str, str] | None = None,
        journal: Sequence[Any] = (),
        calibrations: Sequence[Any] = (),
        extra: Mapping[str, Any] | None = None,
        *,
        dirty: bool = True,
    ) -> None:
        """Create a project.

        `raw` must have unique non-empty string column names, float64 columns and a default row index.
        Raw columns without an entry in `parameters` get a default `ParameterMeta`. A new project starts
        dirty (unsaved); a loader passes `dirty=False`.
        """
        _validate_raw(raw)
        # pandas copy-on-write: this shallow copy shares memory, but writes through either side never
        # reach the other, so neither the caller nor views handed out by `raw` can alter stored data.
        self._raw: pd.DataFrame = raw.copy(deep=False)
        self._formulas: dict[str, str] = self._checked_formulas(formulas or {})
        self._meta: ProjectMeta = self._checked_meta(meta if meta is not None else ProjectMeta())
        self._parameters: dict[str, ParameterMeta] = self._checked_parameters(parameters or {})
        self._journal: list[Any] = copy.deepcopy(list(journal))
        self._calibrations: list[Any] = copy.deepcopy(list(calibrations))
        self._extra: Mapping[str, Any] = _frozen_extra(extra or {}, RESERVED_KEYS, "Project")
        self._dirty = dirty
        self._observers: list[ProjectObserver] = []

    # --- validation helpers -------------------------------------------------------------------------

    def _checked_formulas(self, formulas: Mapping[str, str]) -> dict[str, str]:
        result: dict[str, str] = {}
        for name, text in formulas.items():
            if not isinstance(name, str) or not name or not isinstance(text, str):
                raise ProjectValidationError(f"Formula {name!r} must map a parameter name to a string.")
            if name in self._raw.columns:
                raise ProjectValidationError(
                    f"Formula for {name!r} would overwrite a raw parameter; "
                    "formulas define new parameters only."
                )
            result[name] = text
        return result

    def _checked_meta(self, meta: ProjectMeta) -> ProjectMeta:
        if not isinstance(meta, ProjectMeta):
            raise ProjectValidationError(f"Project metadata must be ProjectMeta, got {type(meta).__name__}.")
        if meta.time_column is not None and meta.time_column not in self._raw.columns:
            raise ProjectValidationError(f"Time column {meta.time_column!r} is not a raw parameter.")
        return meta

    def _checked_parameters(self, parameters: Mapping[str, ParameterMeta]) -> dict[str, ParameterMeta]:
        for key, param in parameters.items():
            if not isinstance(param, ParameterMeta):
                raise ProjectValidationError(f"Parameter {key!r}: expected ParameterMeta, got {param!r}.")
            if key != param.name:
                raise ProjectValidationError(f"Parameter stored under {key!r} is named {param.name!r}.")
        unknown = [n for n in parameters if n not in self._raw.columns and n not in self._formulas]
        if unknown:
            raise ProjectValidationError(
                f"Parameters {', '.join(map(repr, unknown))} are neither raw columns nor defined by formulas."
            )
        result: dict[str, ParameterMeta] = {}
        for name in self._raw.columns:
            param = parameters.get(name, ParameterMeta(name))
            if param.source is not ParameterSource.RAW:
                raise ProjectValidationError(
                    f"Parameter {name!r} is a raw column but is marked {param.source}."
                )
            result[name] = param
        for name in self._formulas:
            param = parameters.get(name, ParameterMeta(name, source=ParameterSource.DERIVED))
            if param.source is not ParameterSource.DERIVED:
                raise ProjectValidationError(f"Parameter {name!r} is defined by a formula but is marked raw.")
            result[name] = param
        return result

    # --- read access --------------------------------------------------------------------------------

    @property
    def raw(self) -> pd.DataFrame:
        """The raw data. A copy-on-write view: changing it never changes the project."""
        return self._raw.copy(deep=False)

    @property
    def n_rows(self) -> int:
        return len(self._raw)

    @property
    def raw_columns(self) -> tuple[str, ...]:
        return tuple(self._raw.columns)

    @property
    def meta(self) -> ProjectMeta:
        return self._meta

    @property
    def parameters(self) -> Mapping[str, ParameterMeta]:
        """Raw parameters in column order, then derived ones. Read-only."""
        return MappingProxyType(self._parameters)

    @property
    def formulas(self) -> Mapping[str, str]:
        """Derived parameter name -> formula text. Read-only."""
        return MappingProxyType(self._formulas)

    @property
    def journal(self) -> tuple[Any, ...]:
        return tuple(copy.deepcopy(self._journal))

    @property
    def calibrations(self) -> tuple[Any, ...]:
        return tuple(copy.deepcopy(self._calibrations))

    @property
    def extra(self) -> Mapping[str, Any]:
        """Top-level project.json fields this GRAD does not know; kept for round trips. Read-only."""
        return self._extra

    @property
    def dirty(self) -> bool:
        """True if the project has changes that are not saved."""
        return self._dirty

    def time(self) -> np.ndarray:
        """Time of every sample, float64.

        The time column if one is set; otherwise `arange(n) / sample_rate_hz`, starting at 0.
        Raises `TimeBaseError` if neither is known.
        """
        if self._meta.time_column is not None:
            return self._raw[self._meta.time_column].to_numpy()
        if self._meta.sample_rate_hz is not None:
            return np.arange(self.n_rows, dtype=np.float64) / self._meta.sample_rate_hz
        raise TimeBaseError("Time is unknown: set a time column or a sample rate for the project.")

    # --- changes ------------------------------------------------------------------------------------

    def subscribe(self, observer: ProjectObserver) -> Callable[[], None]:
        """Call `observer(change)` after every change. Returns a function that unsubscribes it."""
        self._observers.append(observer)

        def unsubscribe() -> None:
            if observer in self._observers:
                self._observers.remove(observer)

        return unsubscribe

    def _changed(self, change: ProjectChange, *, dirty: bool = True) -> None:
        self._dirty = dirty
        for observer in list(self._observers):
            observer(change)

    def set_meta(self, meta: ProjectMeta) -> None:
        """Replace the project metadata."""
        self._meta = self._checked_meta(meta)
        self._changed(ProjectChange.META)

    def update_meta(self, **changes: Any) -> None:
        """Change some metadata fields, e.g. `update_meta(title="Flight 12", sample_rate_hz=128.0)`."""
        self.set_meta(replace(self._meta, **changes))

    def set_parameter(self, param: ParameterMeta) -> None:
        """Replace the info of an existing parameter."""
        if param.name not in self._parameters:
            raise ProjectValidationError(f"There is no parameter named {param.name!r}.")
        parameters = dict(self._parameters)
        parameters[param.name] = param
        self._parameters = self._checked_parameters(parameters)
        self._changed(ProjectChange.PARAMETERS)

    def update_parameter(self, name: str, /, **changes: Any) -> None:
        """Change some fields of a parameter's info, e.g. `update_parameter("load", unit="kN")`."""
        if name not in self._parameters:
            raise ProjectValidationError(f"There is no parameter named {name!r}.")
        if changes.get("name", name) != name:
            raise ProjectValidationError(
                "Renaming a parameter is a journal operation, not a metadata change."
            )
        self.set_parameter(replace(self._parameters[name], **changes))

    def mark_saved(self, modified: datetime) -> None:
        """Record a successful save at `modified`: update the metadata and clear the dirty flag."""
        self._meta = self._checked_meta(replace(self._meta, modified=modified))
        self._changed(ProjectChange.SAVED, dirty=False)
