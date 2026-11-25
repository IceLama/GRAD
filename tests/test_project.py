from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
import pytest

from grad.core.errors import GradError, ProjectValidationError, TimeBaseError
from grad.core.project import (
    ParameterMeta,
    ParameterSource,
    Project,
    ProjectChange,
    ProjectMeta,
)

if TYPE_CHECKING:
    from conftest import FlightDataFactory

ODD_NAMES = {"load": "Нагрузка, кН", "bridge_1": "Мост 1.T", "bridge_2": "bridge 2 (raw).v"}


def frame(**columns: Any) -> pd.DataFrame:
    return pd.DataFrame({name: np.asarray(values, dtype=np.float64) for name, values in columns.items()})


# --- construction and validation ------------------------------------------------------------------------


def test_new_project_fills_raw_parameters_in_column_order(flight_data_factory: "FlightDataFactory") -> None:
    flight = flight_data_factory(duration=2.0, names=ODD_NAMES)
    project = Project(flight.data, ProjectMeta(title="Полёт 1", time_column="Time"))

    assert project.raw_columns == tuple(flight.data.columns)
    assert list(project.parameters) == list(flight.data.columns)
    for name, param in project.parameters.items():
        assert param == ParameterMeta(name, source=ParameterSource.RAW)
    assert project.n_rows == len(flight.data)
    assert project.dirty
    assert project.formulas == {}
    assert project.journal == ()
    assert project.calibrations == ()
    assert project.extra == {}


def test_given_parameter_meta_is_kept() -> None:
    load = ParameterMeta("Нагрузка, кН", unit="кН", description="Сила на штоке")
    project = Project(frame(**{"Нагрузка, кН": [1.0], "x": [2.0]}), parameters={load.name: load})
    assert project.parameters["Нагрузка, кН"] is load
    assert project.parameters["x"] == ParameterMeta("x")


@pytest.mark.parametrize(
    "bad",
    [
        pd.DataFrame({"i": [1, 2]}),
        pd.DataFrame({"f32": np.array([1.0], dtype=np.float32)}),
        pd.DataFrame({"s": ["a"]}),
        pd.DataFrame({"nullable": pd.array([1.0, None], dtype="Float64")}),
    ],
    ids=["int64", "float32", "str", "nullable-Float64"],
)
def test_rejects_non_float64_columns(bad: pd.DataFrame) -> None:
    with pytest.raises(ProjectValidationError, match="float64"):
        Project(bad)


def test_rejects_duplicate_names() -> None:
    data = pd.DataFrame(np.zeros((2, 3)), columns=["a", "Мост", "a"])
    with pytest.raises(ProjectValidationError, match="repeated: a"):
        Project(data)


@pytest.mark.parametrize("name", [0, "", ("a", "b")])
def test_rejects_bad_column_names(name: object) -> None:
    data = pd.DataFrame({name: [1.0]})
    with pytest.raises(ProjectValidationError, match="non-empty strings"):
        Project(data)


def test_rejects_non_default_index() -> None:
    data = frame(a=[1.0, 2.0, 3.0]).iloc[1:]
    with pytest.raises(ProjectValidationError, match="row index"):
        Project(data)
    Project(data.reset_index(drop=True))


def test_rejects_rows_without_columns() -> None:
    with pytest.raises(ProjectValidationError, match="no columns"):
        Project(pd.DataFrame(index=pd.RangeIndex(3)))


def test_rejects_non_dataframe() -> None:
    with pytest.raises(ProjectValidationError, match="DataFrame"):
        Project({"a": [1.0]})  # type: ignore[arg-type]


def test_empty_and_wide_data_are_valid() -> None:
    assert Project(pd.DataFrame()).n_rows == 0
    assert Project(frame(a=[], b=[])).raw_columns == ("a", "b")
    wide = pd.DataFrame(np.ones((2, 50)), columns=[f"p.{i} м" for i in range(50)])
    assert Project(wide).raw_columns == tuple(wide.columns)


def test_rejects_unknown_time_column() -> None:
    with pytest.raises(ProjectValidationError, match="Time column 'Время'"):
        Project(frame(a=[1.0]), ProjectMeta(time_column="Время"))


@pytest.mark.parametrize("rate", [0.0, -1.0, float("nan"), float("inf"), "128", True])
def test_rejects_bad_sample_rate(rate: object) -> None:
    with pytest.raises(ProjectValidationError, match="Sample rate"):
        ProjectMeta(sample_rate_hz=rate)  # type: ignore[arg-type]


def test_meta_normalises_values() -> None:
    meta = ProjectMeta(sample_rate_hz=128, source_files=["a.txt", "б.csv"])  # type: ignore[arg-type]
    assert meta.sample_rate_hz == 128.0
    assert isinstance(meta.sample_rate_hz, float)
    assert meta.source_files == ("a.txt", "б.csv")
    assert meta.created.tzinfo is not None
    with pytest.raises(FrozenInstanceError):
        meta.title = "x"  # type: ignore[misc]


def test_meta_rejects_naive_datetime_and_bad_source_files() -> None:
    with pytest.raises(ProjectValidationError, match="time zone"):
        ProjectMeta(created=datetime(2026, 1, 1))
    with pytest.raises(ProjectValidationError, match="Source files"):
        ProjectMeta(source_files="a.txt")  # type: ignore[arg-type]


def test_extra_fields_must_not_shadow_known_keys() -> None:
    with pytest.raises(ProjectValidationError, match="reserved keys: title"):
        ProjectMeta(extra={"title": "x"})
    with pytest.raises(ProjectValidationError, match="reserved keys: unit"):
        ParameterMeta("a", extra={"unit": "m"})
    with pytest.raises(ProjectValidationError, match="reserved keys: journal"):
        Project(frame(a=[1.0]), extra={"journal": []})


def test_extra_fields_are_copied() -> None:
    source = {"tags": ["a"]}
    meta = ProjectMeta(extra=source)
    source["tags"].append("b")
    assert meta.extra == {"tags": ["a"]}


def test_parameter_meta_validation() -> None:
    assert ParameterMeta("a", source="derived").source is ParameterSource.DERIVED  # type: ignore[arg-type]
    with pytest.raises(ProjectValidationError, match="unknown source"):
        ParameterMeta("a", source="computed")  # type: ignore[arg-type]
    with pytest.raises(ProjectValidationError, match="non-empty string"):
        ParameterMeta("")


def test_parameter_consistency_checks() -> None:
    data = frame(a=[1.0])
    with pytest.raises(ProjectValidationError, match="stored under 'a' is named 'b'"):
        Project(data, parameters={"a": ParameterMeta("b")})
    with pytest.raises(ProjectValidationError, match="neither raw columns nor defined by formulas"):
        Project(data, parameters={"ghost": ParameterMeta("ghost")})
    with pytest.raises(ProjectValidationError, match="raw column but is marked derived"):
        Project(data, parameters={"a": ParameterMeta("a", source=ParameterSource.DERIVED)})


def test_formulas_define_derived_parameters_only() -> None:
    data = frame(a=[1.0])
    project = Project(data, formulas={"a_h": "a - 1"})
    assert project.parameters["a_h"].source is ParameterSource.DERIVED
    assert list(project.parameters) == ["a", "a_h"]
    with pytest.raises(ProjectValidationError, match="overwrite a raw parameter"):
        Project(data, formulas={"a": "a * 2"})
    with pytest.raises(ProjectValidationError, match="defined by a formula but is marked raw"):
        Project(data, formulas={"b": "a"}, parameters={"b": ParameterMeta("b")})


# --- raw data is immutable --------------------------------------------------------------------------------


def test_raw_view_changes_do_not_reach_project() -> None:
    project = Project(frame(a=[1.0, 2.0], b=[3.0, 4.0]))
    view = project.raw
    view.loc[0, "a"] = 100.0
    view["c"] = 0.0
    del view["b"]
    assert project.raw.equals(frame(a=[1.0, 2.0], b=[3.0, 4.0]))


def test_raw_numpy_arrays_are_read_only() -> None:
    project = Project(frame(a=[1.0, 2.0]), ProjectMeta(time_column="a"))
    with pytest.raises(ValueError, match="read-only"):
        project.raw["a"].to_numpy()[0] = 5.0
    with pytest.raises(ValueError, match="read-only"):
        project.time()[0] = 5.0


def test_changing_the_source_frame_does_not_reach_project() -> None:
    source = frame(a=[1.0, 2.0])
    project = Project(source)
    source.loc[0, "a"] = -1.0
    source["a"] = 7.0
    assert project.raw["a"].tolist() == [1.0, 2.0]


def test_collections_are_read_only() -> None:
    project = Project(frame(a=[1.0]), formulas={"b": "a"}, journal=[{"op": "x"}])
    with pytest.raises(TypeError):
        project.parameters["a"] = ParameterMeta("a")  # type: ignore[index]
    with pytest.raises(TypeError):
        project.formulas["c"] = "a"  # type: ignore[index]
    project.journal[0]["op"] = "changed"
    assert project.journal == ({"op": "x"},)


# --- time -------------------------------------------------------------------------------------------------


def test_time_from_time_column_is_returned_exactly() -> None:
    t = np.array([0.0, 0.1, 0.25, 0.26, 1.7, np.nan])  # non-uniform, with a gap value
    project = Project(frame(t=t, x=np.zeros(6)), ProjectMeta(time_column="t", sample_rate_hz=10.0))
    assert np.array_equal(project.time(), t, equal_nan=True)
    assert project.time().dtype == np.float64


@pytest.mark.parametrize("fs", [128.0, 64.0, 1000.0, 0.5, 1 / 3])
def test_time_from_sample_rate_starts_at_zero(fs: float) -> None:
    n = 1001
    project = Project(frame(x=np.zeros(n)), ProjectMeta(sample_rate_hz=fs))
    t = project.time()
    assert t[0] == 0.0
    assert np.array_equal(t, np.arange(n, dtype=np.float64) / fs)
    assert t.dtype == np.float64


def test_time_with_cyrillic_time_column(flight_data_factory: "FlightDataFactory") -> None:
    flight = flight_data_factory(duration=1.0, names={"time": "Время, с"})
    project = Project(flight.data, ProjectMeta(time_column="Время, с"))
    assert np.array_equal(project.time(), flight.data["Время, с"].to_numpy())


def test_time_of_empty_project() -> None:
    assert len(Project(pd.DataFrame(), ProjectMeta(sample_rate_hz=10.0)).time()) == 0
    assert len(Project(frame(t=[]), ProjectMeta(time_column="t")).time()) == 0


def test_time_unknown_raises() -> None:
    project = Project(frame(x=[1.0, 2.0]))
    with pytest.raises(TimeBaseError) as info:
        project.time()
    assert isinstance(info.value, GradError)


# --- changes, dirty flag, observers -----------------------------------------------------------------------


def test_loaded_project_starts_clean() -> None:
    assert not Project(frame(a=[1.0]), dirty=False).dirty


def test_update_meta_marks_dirty_and_notifies() -> None:
    project = Project(frame(a=[1.0]), dirty=False)
    changes: list[ProjectChange] = []
    project.subscribe(changes.append)

    project.update_meta(title="Полёт 12", sample_rate_hz=128.0, time_column="a")

    assert project.meta.title == "Полёт 12"
    assert project.meta.sample_rate_hz == 128.0
    assert project.dirty
    assert changes == [ProjectChange.META]


def test_invalid_change_leaves_project_untouched() -> None:
    project = Project(frame(a=[1.0]), dirty=False)
    changes: list[ProjectChange] = []
    project.subscribe(changes.append)
    before = project.meta

    with pytest.raises(ProjectValidationError):
        project.update_meta(time_column="missing")
    with pytest.raises(ProjectValidationError):
        project.update_meta(sample_rate_hz=-5.0)
    with pytest.raises(ProjectValidationError):
        project.update_parameter("missing", unit="m")

    assert project.meta is before
    assert not project.dirty
    assert changes == []


def test_update_parameter() -> None:
    project = Project(frame(**{"Мост 1.T": [1.0]}), dirty=False)
    changes: list[ProjectChange] = []
    project.subscribe(changes.append)

    project.update_parameter("Мост 1.T", unit="мВ/В", description="Тензомост 1")

    assert project.parameters["Мост 1.T"] == ParameterMeta("Мост 1.T", "мВ/В", "Тензомост 1")
    assert project.dirty
    assert changes == [ProjectChange.PARAMETERS]
    with pytest.raises(ProjectValidationError, match="journal operation"):
        project.update_parameter("Мост 1.T", name="Мост 2")
    with pytest.raises(ProjectValidationError, match="marked derived"):
        project.update_parameter("Мост 1.T", source=ParameterSource.DERIVED)


def test_mark_saved_clears_dirty_and_sets_modified() -> None:
    project = Project(frame(a=[1.0]))
    changes: list[ProjectChange] = []
    project.subscribe(changes.append)
    saved_at = datetime(2026, 11, 25, 12, 0, tzinfo=timezone(timedelta(hours=3)))

    project.mark_saved(saved_at)

    assert not project.dirty
    assert project.meta.modified == saved_at
    assert changes == [ProjectChange.SAVED]


def test_unsubscribe_and_unsubscribe_during_notification() -> None:
    project = Project(frame(a=[1.0]))
    calls: list[str] = []

    def once(change: ProjectChange) -> None:
        calls.append(f"once:{change}")
        unsubscribe_once()

    unsubscribe_once = project.subscribe(once)
    unsubscribe_other = project.subscribe(lambda change: calls.append(f"other:{change}"))

    project.update_meta(title="1")
    project.update_meta(title="2")
    unsubscribe_other()
    unsubscribe_other()  # idempotent
    project.update_meta(title="3")

    assert calls == ["once:meta", "other:meta", "other:meta"]


def test_observer_errors_propagate() -> None:
    project = Project(frame(a=[1.0]))

    def broken(change: ProjectChange) -> None:
        raise RuntimeError("observer failed")

    project.subscribe(broken)
    with pytest.raises(RuntimeError, match="observer failed"):
        project.update_meta(title="x")


def test_created_is_not_touched_by_changes() -> None:
    created = datetime(2020, 5, 1, tzinfo=UTC)
    project = Project(frame(a=[1.0]), ProjectMeta(created=created))
    project.update_meta(notes="Заметка")
    project.mark_saved(datetime(2026, 1, 1, tzinfo=UTC))
    assert project.meta.created == created
