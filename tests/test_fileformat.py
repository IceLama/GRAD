import io
import json
import struct
import zipfile
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from grad.core import fileformat
from grad.core.errors import GradError, GradFileError, ProjectFileError, UnsupportedVersionError
from grad.core.fileformat import JSON_ENTRY, RAW_ENTRY, SCHEMA_VERSION, load, save
from grad.core.project import ParameterMeta, ParameterSource, Project, ProjectMeta

if TYPE_CHECKING:
    from conftest import FlightDataFactory

ODD_NAMES = {
    "time": "Время, с",
    "sine": "sine.amp 1",
    "noise": "__index_level_0__",
    "load": "Нагрузка, кН",
    "bridge_1": "Мост 1.T",
    "bridge_2": "Unnamed: 0",
}


def bits(value: int) -> float:
    return struct.unpack("<d", struct.pack("<Q", value))[0]


def assert_bit_exact(actual: pd.DataFrame, expected: pd.DataFrame) -> None:
    assert list(actual.columns) == list(expected.columns)
    assert all(dtype == np.float64 for dtype in actual.dtypes)
    for name in expected.columns:
        a = actual[name].to_numpy().view(np.uint64)
        e = expected[name].to_numpy().view(np.uint64)
        assert np.array_equal(a, e), name


def make_project(**kwargs: Any) -> Project:
    data = pd.DataFrame({"Time": [0.0, 0.5, 1.0], "Мост 1.T": [1.0, np.nan, -2.5]})
    return Project(data, ProjectMeta(title="Полёт", time_column="Time", sample_rate_hz=2.0), **kwargs)


def read_entries(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path) as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def write_entries(path: Path, entries: dict[str, bytes]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_STORED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)


def edit_json(path: Path, edit: Callable[[dict[str, Any]], None]) -> None:
    entries = read_entries(path)
    document = json.loads(entries[JSON_ENTRY])
    edit(document)
    entries[JSON_ENTRY] = json.dumps(document, ensure_ascii=False).encode("utf-8")
    write_entries(path, entries)


def parquet_bytes(table: pa.Table) -> bytes:
    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    return buffer.getvalue()


# --- round trip --------------------------------------------------------------------------------------------


def test_round_trip_is_bit_exact(tmp_path: Path) -> None:
    special = np.array(
        [
            0.0,
            -0.0,
            np.inf,
            -np.inf,
            np.nan,
            bits(0xFFF8000000000000),  # negative quiet NaN
            bits(0x7FF8000000000123),  # NaN with payload
            bits(0x7FF0000000000001),  # signalling NaN
            5e-324,  # smallest subnormal
            2.2250738585072014e-308,
            1.7976931348623157e308,
            0.1,
            1 / 3,
        ]
    )
    rng = np.random.default_rng(42)
    random_bits = rng.integers(0, 2**64, size=10_000, dtype=np.uint64).view(np.float64)
    data = pd.DataFrame(
        {
            "special": np.resize(special, len(random_bits)),
            "random bits": random_bits,
            "Мост 1.T": rng.normal(size=len(random_bits)),
        }
    )
    save(Project(data), tmp_path / "p.gradproj")
    assert_bit_exact(load(tmp_path / "p.gradproj").raw, data)


def test_round_trip_keeps_metadata_and_odd_names(
    tmp_path: Path, flight_data_factory: "FlightDataFactory"
) -> None:
    flight = flight_data_factory(duration=3.0, nan_gaps=[(1.0, 1.5)], names=ODD_NAMES)
    created = datetime(2025, 3, 1, 9, 30, 15, 123456, tzinfo=UTC)
    meta = ProjectMeta(
        title="Полёт №7: «режим 2»",
        created=created,
        modified=created,
        sample_rate_hz=flight.fs,
        time_column="Время, с",
        source_files=("C:/Данные/полёт 7.txt", "b.csv"),
        notes='Многострочная\nзаметка; с разделителями, «кавычками» и "quotes"',
    )
    parameters = {
        "Нагрузка, кН": ParameterMeta("Нагрузка, кН", unit="кН", description="Сила на штоке"),
        "Мост 1.T": ParameterMeta("Мост 1.T", unit="мВ/В"),
    }
    project = Project(flight.data, meta, parameters)
    path = tmp_path / "полёт 7.v2.gradproj"

    save(project, path)
    loaded = load(path)

    assert_bit_exact(loaded.raw, flight.data)
    assert loaded.meta == project.meta
    assert loaded.meta.created == created
    assert loaded.meta.modified == project.meta.modified
    assert dict(loaded.parameters) == dict(project.parameters)
    assert list(loaded.parameters) == list(flight.data.columns)
    assert np.array_equal(loaded.time(), project.time())


def test_save_marks_clean_and_updates_modified(tmp_path: Path) -> None:
    project = make_project()
    before = project.meta
    changes: list[str] = []
    project.subscribe(lambda change: changes.append(change))

    save(project, tmp_path / "p.gradproj")

    assert not project.dirty
    assert changes == ["saved"]
    assert project.meta.modified > before.modified
    assert project.meta.created == before.created
    loaded = load(tmp_path / "p.gradproj")
    assert not loaded.dirty
    assert loaded.meta.modified == project.meta.modified


def test_formulas_journal_and_calibrations_round_trip(tmp_path: Path) -> None:
    project = make_project(
        formulas={"Мост 1.T_h": "`Мост 1.T` - 1"},
        parameters={"Мост 1.T_h": ParameterMeta("Мост 1.T_h", unit="мВ/В", source=ParameterSource.DERIVED)},
        journal=[{"op": "time_shift", "seconds": 0.25}],
        calibrations=[{"name": "К1", "coefficients": [1.5, -0.25]}],
    )
    save(project, tmp_path / "p.gradproj")
    loaded = load(tmp_path / "p.gradproj")
    assert loaded.formulas == project.formulas
    assert loaded.parameters["Мост 1.T_h"] == project.parameters["Мост 1.T_h"]
    assert loaded.journal == project.journal
    assert loaded.calibrations == project.calibrations


@pytest.mark.parametrize(
    "data",
    [
        pd.DataFrame(),
        pd.DataFrame({"a": np.array([], dtype=np.float64), "б в.г": np.array([], dtype=np.float64)}),
        pd.DataFrame(np.arange(60.0).reshape(2, 30), columns=[f"канал {i}.x" for i in range(30)]),
        pd.DataFrame({"only NaN": [np.nan, np.nan]}),
    ],
    ids=["no-columns", "no-rows", "more-columns-than-rows", "all-nan"],
)
def test_round_trip_edge_shapes(tmp_path: Path, data: pd.DataFrame) -> None:
    save(Project(data), tmp_path / "p.gradproj")
    loaded = load(tmp_path / "p.gradproj")
    assert loaded.raw_columns == tuple(data.columns)
    assert loaded.n_rows == len(data)
    assert_bit_exact(loaded.raw, data)


def test_archive_layout(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)

    with zipfile.ZipFile(path) as archive:
        infos = archive.infolist()
        assert sorted(i.filename for i in infos) == [JSON_ENTRY, RAW_ENTRY]
        assert all(i.compress_type == zipfile.ZIP_STORED for i in infos)
        document = json.loads(archive.read(JSON_ENTRY).decode("utf-8"))
        table = pq.read_table(io.BytesIO(archive.read(RAW_ENTRY)))

    assert document["schema_version"] == SCHEMA_VERSION == 1
    assert set(document) == {"schema_version", "meta", "parameters", "formulas", "journal", "calibrations"}
    assert document["meta"]["title"] == "Полёт"
    assert [p["name"] for p in document["parameters"]] == ["Time", "Мост 1.T"]
    assert table.column_names == ["Time", "Мост 1.T"]
    assert all(f.type == pa.float64() for f in table.schema)
    assert list(tmp_path.iterdir()) == [path]  # no temporary file left


def test_unknown_keys_survive_round_trip(tmp_path: Path) -> None:
    first, second = tmp_path / "a.gradproj", tmp_path / "b.gradproj"
    save(make_project(), first)

    def add_unknown(document: dict[str, Any]) -> None:
        document["future_feature"] = {"enabled": True, "items": [1, "два", None]}
        document["meta"]["aircraft"] = "Ил-114"
        document["parameters"][1]["color"] = "#ff0000"

    edit_json(first, add_unknown)
    loaded = load(first)
    assert loaded.extra == {"future_feature": {"enabled": True, "items": [1, "два", None]}}
    assert loaded.meta.extra == {"aircraft": "Ил-114"}
    assert loaded.parameters["Мост 1.T"].extra == {"color": "#ff0000"}

    save(loaded, second)
    document = json.loads(read_entries(second)[JSON_ENTRY])
    assert document["future_feature"] == {"enabled": True, "items": [1, "два", None]}
    assert document["meta"]["aircraft"] == "Ил-114"
    assert document["parameters"][1]["color"] == "#ff0000"


def test_save_overwrites_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    project = make_project()
    save(project, path)
    project.update_meta(title="Второе имя")
    save(project, path)
    assert load(path).meta.title == "Второе имя"
    assert list(tmp_path.iterdir()) == [path]


# --- failed writes -----------------------------------------------------------------------------------------


@pytest.fixture
def existing(tmp_path: Path) -> tuple[Path, bytes]:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    return path, path.read_bytes()


def test_failed_write_leaves_old_file_intact(
    existing: tuple[Path, bytes], monkeypatch: pytest.MonkeyPatch
) -> None:
    path, old_bytes = existing

    def disk_full(table: pa.Table, where: Any, **kwargs: Any) -> None:
        where.write(b"PAR1 partial data")
        raise OSError(28, "No space left on device")

    monkeypatch.setattr(fileformat.pq, "write_table", disk_full)
    project = make_project()
    modified_before = project.meta.modified

    with pytest.raises(GradFileError, match="No space left on device") as info:
        save(project, path)

    assert isinstance(info.value.__cause__, OSError)
    assert info.value.path == path
    assert path.read_bytes() == old_bytes
    assert list(path.parent.iterdir()) == [path]
    assert project.dirty
    assert project.meta.modified == modified_before


def test_failed_replace_leaves_old_file_intact(
    existing: tuple[Path, bytes], monkeypatch: pytest.MonkeyPatch
) -> None:
    path, old_bytes = existing

    def locked(src: Any, dst: Any) -> None:
        raise PermissionError(13, "Permission denied")

    monkeypatch.setattr(fileformat.os, "replace", locked)
    with pytest.raises(GradFileError, match="Permission denied"):
        save(make_project(), path)
    assert path.read_bytes() == old_bytes
    assert list(path.parent.iterdir()) == [path]


def test_unexpected_error_still_cleans_up(
    existing: tuple[Path, bytes], monkeypatch: pytest.MonkeyPatch
) -> None:
    path, old_bytes = existing

    def bug(*args: Any, **kwargs: Any) -> None:
        raise RuntimeError("bug")

    monkeypatch.setattr(fileformat.pq, "write_table", bug)
    with pytest.raises(RuntimeError, match="bug"):
        save(make_project(), path)
    assert path.read_bytes() == old_bytes
    assert list(path.parent.iterdir()) == [path]


def test_save_to_missing_folder_or_directory(tmp_path: Path) -> None:
    with pytest.raises(GradFileError):
        save(make_project(), tmp_path / "нет такой папки" / "p.gradproj")
    folder = tmp_path / "folder.gradproj"
    folder.mkdir()
    with pytest.raises(GradFileError):
        save(make_project(), folder)
    assert list(folder.iterdir()) == []


# --- damaged and foreign files -----------------------------------------------------------------------------


def test_newer_schema_version_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    edit_json(path, lambda d: d.update(schema_version=SCHEMA_VERSION + 1))

    with pytest.raises(UnsupportedVersionError) as info:
        load(path)
    assert info.value.found == 2
    assert info.value.supported == 1
    assert isinstance(info.value, ProjectFileError)
    assert isinstance(info.value, GradError)
    assert "newer GRAD" in str(info.value)


def test_newer_schema_version_is_reported_before_layout_problems(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    write_entries(path, {JSON_ENTRY: json.dumps({"schema_version": 7, "everything": "else"}).encode()})
    with pytest.raises(UnsupportedVersionError):
        load(path)


@pytest.mark.parametrize("version", [None, 0, -1, "1", 1.0, True])
def test_bad_schema_version(tmp_path: Path, version: object) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    edit_json(path, lambda d: d.update(schema_version=version))
    with pytest.raises(ProjectFileError, match="schema_version"):
        load(path)


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(GradFileError) as info:
        load(tmp_path / "нет.gradproj")
    assert not isinstance(info.value, ProjectFileError)


def test_not_a_zip(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    path.write_text("Time;x\n0;1\n", encoding="utf-8")
    with pytest.raises(ProjectFileError, match="not a ZIP"):
        load(path)


@pytest.mark.parametrize("missing", [JSON_ENTRY, RAW_ENTRY])
def test_missing_entry(tmp_path: Path, missing: str) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    entries = read_entries(path)
    del entries[missing]
    write_entries(path, entries)
    with pytest.raises(ProjectFileError, match=f"no {missing}"):
        load(path)


@pytest.mark.parametrize(
    "content",
    [b"{not json", b"[1, 2]", b'{"schema_version": 1, "x": NaN}', b"\xff\xfe\x00"],
    ids=["syntax", "array", "nan-constant", "not-utf8"],
)
def test_bad_json(tmp_path: Path, content: bytes) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    entries = read_entries(path)
    entries[JSON_ENTRY] = content
    write_entries(path, entries)
    with pytest.raises(ProjectFileError, match=JSON_ENTRY):
        load(path)


@pytest.mark.parametrize(
    ("edit", "message"),
    [
        (lambda d: d["meta"].update(time_column="Нет такого"), "Time column"),
        (lambda d: d["meta"].update(created="вчера"), "ISO 8601"),
        (lambda d: d["meta"].update(created="2026-01-01T10:00:00"), "time zone"),
        (lambda d: d["meta"].update(sample_rate_hz=-1), "Sample rate"),
        (lambda d: d["parameters"].append({"name": "призрак"}), "neither raw columns"),
        (lambda d: d["parameters"].append(dict(d["parameters"][0])), "listed twice"),
        (lambda d: d["parameters"].append("Time"), "JSON object"),
        (lambda d: d.update(formulas={"Time": "1"}), "overwrite a raw parameter"),
        (lambda d: d.pop("journal"), "'journal' is missing"),
        (lambda d: d.update(calibrations={}), "'calibrations' must be a JSON array"),
    ],
)
def test_inconsistent_json(tmp_path: Path, edit: Callable[[dict[str, Any]], None], message: str) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    edit_json(path, edit)
    with pytest.raises(ProjectFileError, match=message):
        load(path)


def test_non_float_parquet_column(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    entries = read_entries(path)
    entries[RAW_ENTRY] = parquet_bytes(pa.table({"Time": [0, 1, 2], "Мост 1.T": [1.0, 2.0, 3.0]}))
    write_entries(path, entries)
    with pytest.raises(ProjectFileError, match="'Time' in raw.parquet is int64"):
        load(path)


def test_repeated_parquet_columns(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    entries = read_entries(path)
    table = pa.Table.from_arrays([pa.array([1.0]), pa.array([2.0])], names=["Time", "Time"])
    entries[RAW_ENTRY] = parquet_bytes(table)
    write_entries(path, entries)
    with pytest.raises(ProjectFileError, match="repeated column names"):
        load(path)


def test_damaged_parquet(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    entries = read_entries(path)
    entries[RAW_ENTRY] = entries[RAW_ENTRY][: len(entries[RAW_ENTRY]) // 2]
    write_entries(path, entries)
    with pytest.raises(ProjectFileError, match="damaged"):
        load(path)


def test_columns_missing_from_json_get_default_parameters(tmp_path: Path) -> None:
    path = tmp_path / "p.gradproj"
    save(make_project(), path)
    edit_json(path, lambda d: d.update(parameters=[]))
    assert load(path).parameters["Мост 1.T"] == ParameterMeta("Мост 1.T")
