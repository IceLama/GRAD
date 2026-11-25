import builtins
import csv
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import pytest

from grad.core.errors import GradFileError, LegacyFormatError
from grad.core.loaders.legacy_grad import (
    FORMULAS_COLUMN,
    NO_FORMULA,
    LegacyFormula,
    LoadWarningCode,
    V1TimePattern,
    detect_v1_time,
    load_legacy_grad,
)
from grad.core.project import Project, ProjectMeta

LEGACY_SAMPLES = sorted((Path(__file__).parent / "data" / "legacy").glob("*.grad"))


def v1_time(n: int, freq: int) -> list[float]:
    """The v1 Time generator, as in GRAD v1 `Parameters.add_parameter` (padding bug included)."""
    dd = [i / 1000 + j for j in range(1, int(n / freq + 1)) for i in range(freq)]
    div = n - len(dd)
    if div != 0:
        dd.extend([i / 1000 + j for j in range(int(dd[-1]), int(dd[-1] + abs(div))) for i in range(freq)])
    return dd[:n]


def cell(value: float | None) -> str:
    """Format a value as v1 (polars) did: shortest round-trip repr, empty cell for a missing value."""
    if value is None:
        return ""
    if np.isnan(value):
        return "NaN"
    return repr(float(value))


def write_v1_grad(
    path: Path,
    columns: Mapping[str, Sequence[float | None]],
    formulas: Mapping[int, str] | None = None,
    *,
    formula_column: bool = True,
    encoding: str = "utf-8",
) -> None:
    """Write a file the way GRAD v1 did: `;`-separated, formula of column i in row i of `__Формулы__`."""
    names = list(columns)
    n = len(next(iter(columns.values()))) if columns else 0
    with open(path, "w", encoding=encoding, newline="") as file:
        writer = csv.writer(file, delimiter=";", lineterminator="\n")
        writer.writerow([*names, FORMULAS_COLUMN] if formula_column else names)
        for row in range(n):
            values = [cell(columns[name][row]) for name in names]
            if formula_column:
                values.append((formulas or {}).get(row, NO_FORMULA))
            writer.writerow(values)


# --- loading -----------------------------------------------------------------------------------------------


def test_loads_v1_file_with_formulas_by_name(tmp_path: Path) -> None:
    fs, n = 8, 8 * 3 + 5
    rng = np.random.default_rng(3)
    time = v1_time(n, fs)
    columns = {
        "Time": time,
        "Нагрузка, кН": list(rng.normal(size=n)),
        "Мост 1.T": list(rng.normal(size=n) * 1e-3),
        "Мост 1.T_0": [1.0] * n,
        "Мост 1.T_h": list(rng.normal(size=n)),
        "имя; с разделителем": list(rng.normal(size=n)),
        "L": [0.728] * n,
    }
    formulas = {
        3: "1.0",
        4: "Мост 1.T - Мост 1.T_0",
        6: "data.loc[:, 'L'] = np.where((data['Time'] > 0) & (data['Time'] <= data['t2']), "
        "0.728, data['L']);",
    }
    path = tmp_path / "полёт 7.grad"
    write_v1_grad(path, columns, formulas)

    result = load_legacy_grad(path)

    expected = pd.DataFrame({name: np.asarray(v, dtype=np.float64) for name, v in columns.items()})
    assert list(result.data.columns) == list(columns)
    for name in columns:
        assert np.array_equal(
            result.data[name].to_numpy().view(np.uint64), expected[name].to_numpy().view(np.uint64)
        )
    assert result.formulas == {
        "Мост 1.T_0": LegacyFormula("1.0", legacy_python=False),
        "Мост 1.T_h": LegacyFormula("Мост 1.T - Мост 1.T_0", legacy_python=False),
        "L": LegacyFormula(formulas[6], legacy_python=True),
    }
    assert result.time_column == "Time"
    assert result.v1_time == V1TimePattern(sample_rate_hz=8.0, start_second=1, repeated_tail=5)
    assert [w.code for w in result.warnings] == [LoadWarningCode.V1_GENERATED_TIME]
    assert "arange(n) / 8" in result.warnings[0].message
    assert "last 5 samples repeat" in result.warnings[0].message


def test_result_is_ready_for_a_project(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"Time": v1_time(20, 4), "x": [0.5] * 20})
    result = load_legacy_grad(path)
    project = Project(result.data, ProjectMeta(time_column=result.time_column, sample_rate_hz=4.0))
    assert project.raw_columns == ("Time", "x")


def test_formula_text_is_kept_exactly(tmp_path: Path) -> None:
    texts = {
        0: "  x * 2  ",
        1: 'np.where(x > 0; "a"; "b")',
        2: "  data.loc[:, 'y'] = 1",
        3: "x + data.loc[:, 'y']",
    }
    path = tmp_path / "a.grad"
    write_v1_grad(path, {name: [1.0] * 5 for name in ("x", "y", "z", "w")}, texts)
    formulas = load_legacy_grad(path).formulas
    assert {name: f.text for name, f in formulas.items()} == dict(zip("xyzw", texts.values(), strict=True))
    assert {name: f.legacy_python for name, f in formulas.items()} == {
        "x": False,
        "y": False,
        "z": True,
        "w": False,
    }


def test_formulas_are_never_executed(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("formula was executed")

    monkeypatch.setattr(builtins, "exec", forbidden)
    monkeypatch.setattr(builtins, "eval", forbidden)
    path = tmp_path / "a.grad"
    payload = "data.loc[:, 'x'] = __import__('os').system('exit 3')"
    write_v1_grad(path, {"x": [1.0, 2.0]}, {0: payload})
    assert load_legacy_grad(path).formulas["x"] == LegacyFormula(payload, legacy_python=True)


def test_missing_formula_column_loads_all_columns_with_warning(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"a": [1.0, 2.0], "б.в г": [3.0, 4.0]}, formula_column=False)
    result = load_legacy_grad(path)
    assert list(result.data.columns) == ["a", "б.в г"]
    assert result.formulas == {}
    assert [w.code for w in result.warnings] == [LoadWarningCode.NO_FORMULAS_COLUMN]
    assert result.time_column is None


def test_more_columns_than_rows(tmp_path: Path) -> None:
    names = [f"канал {i}.x" for i in range(6)]
    path = tmp_path / "a.grad"
    write_v1_grad(
        path, {name: [float(i), float(i) + 0.5] for i, name in enumerate(names)}, {0: "1.0", 1: "a+b"}
    )
    result = load_legacy_grad(path)
    assert list(result.data.columns) == names
    assert result.data.shape == (2, 6)
    assert dict(result.formulas) == {
        "канал 0.x": LegacyFormula("1.0", False),
        "канал 1.x": LegacyFormula("a+b", False),
    }
    assert result.warnings == ()


def test_formula_cells_below_last_parameter_are_reported(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"a": [1.0] * 6, "b": [2.0] * 6}, {1: "a * 2", 4: "orphan", 5: "orphan 2"})
    result = load_legacy_grad(path)
    assert dict(result.formulas) == {"b": LegacyFormula("a * 2", False)}
    assert [w.code for w in result.warnings] == [LoadWarningCode.UNASSIGNED_FORMULAS]
    assert result.warnings[0].message.startswith("2 formula cell(s)")


def test_missing_values_and_special_numbers(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text(
        "a;b;__Формулы__\n"
        "1;;no formula\n"
        "NaN;inf;no formula\n"
        "-0.0;-inf;no formula\n"
        "1e-300;NA;no formula\n"
        "2.5E+3;null;no formula\n",
        encoding="utf-8",
    )
    data = load_legacy_grad(path).data
    a, b = data["a"].to_numpy(), data["b"].to_numpy()
    assert np.array_equal(a, [1.0, np.nan, -0.0, 1e-300, 2500.0], equal_nan=True)
    assert np.signbit(a[2])
    assert np.array_equal(b, [np.nan, np.inf, -np.inf, np.nan, np.nan], equal_nan=True)
    assert all(dtype == np.float64 for dtype in data.dtypes)


def test_floats_are_read_exactly(tmp_path: Path) -> None:
    rng = np.random.default_rng(0)
    raw_bits = rng.integers(0, 2**64, size=5000, dtype=np.uint64).view(np.float64)
    values = np.concatenate([raw_bits[np.isfinite(raw_bits)], [0.1, 0.30000000000000004, 5e-324]])
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"x": list(values)})
    loaded = load_legacy_grad(path).data["x"].to_numpy()
    assert np.array_equal(loaded.view(np.uint64), values.view(np.uint64))


def test_short_rows_give_nan_and_no_formula(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text("a;b;__Формулы__\n1;2;x\n3\n", encoding="utf-8")
    result = load_legacy_grad(path)
    assert np.array_equal(result.data["b"].to_numpy(), [2.0, np.nan], equal_nan=True)
    assert dict(result.formulas) == {"a": LegacyFormula("x", False)}


def test_header_only(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text("Time;a;__Формулы__\n", encoding="utf-8")
    result = load_legacy_grad(path)
    assert result.data.shape == (0, 2)
    assert result.formulas == {}
    assert result.v1_time is None


def test_byte_order_mark_is_accepted(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"Нагрузка": [1.0]}, encoding="utf-8-sig")
    assert list(load_legacy_grad(path).data.columns) == ["Нагрузка"]


def test_dotted_names_that_pandas_would_invent_are_kept(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"a": [1.0], "a.1": [2.0], "Unnamed: 0": [3.0]})
    assert list(load_legacy_grad(path).data.columns) == ["a", "a.1", "Unnamed: 0"]


# --- errors ------------------------------------------------------------------------------------------------


def test_repeated_names_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text("Мост;x;Мост;__Формулы__\n1;2;3;no formula\n", encoding="utf-8")
    with pytest.raises(LegacyFormatError, match="repeat: Мост") as info:
        load_legacy_grad(path)
    assert info.value.column == "Мост"


def test_empty_name_is_rejected(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text("a;;__Формулы__\n1;2;no formula\n", encoding="utf-8")
    with pytest.raises(LegacyFormatError, match="column 2 has no name"):
        load_legacy_grad(path)


def test_formula_column_must_be_last(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text("a;__Формулы__;b\n1;no formula;2\n", encoding="utf-8")
    with pytest.raises(LegacyFormatError, match="must be the last"):
        load_legacy_grad(path)


def test_non_numeric_value_names_column_and_line(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_text(
        "a;Мост 1.T;__Формулы__\n1;inf;no formula\n2;-inf;no formula\n3;1,5;no formula\n", encoding="utf-8"
    )
    with pytest.raises(LegacyFormatError, match=r"line 4: value '1,5' in column 'Мост 1.T'") as info:
        load_legacy_grad(path)
    assert info.value.column == "Мост 1.T"
    assert info.value.line == 4


@pytest.mark.parametrize(
    "body",
    [
        "1;no formula;7;8\n",
        "1;no formula;7\n2;no formula\n",
        "1;no formula\n2;no formula;7\n",
        "1;no formula;\n",
    ],
    ids=["every-row", "first-row", "later-row", "trailing-separator"],
)
def test_too_many_fields_is_rejected(tmp_path: Path, body: str) -> None:
    # pandas would otherwise shift values into the row index or drop the extra fields.
    path = tmp_path / "a.grad"
    path.write_text("a;__Формулы__\n" + body, encoding="utf-8")
    with pytest.raises(LegacyFormatError, match="not a valid"):
        load_legacy_grad(path)


def test_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    path.write_bytes(b"")
    with pytest.raises(LegacyFormatError, match="empty"):
        load_legacy_grad(path)


def test_non_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"Нагрузка": [1.0]}, encoding="cp1251")
    with pytest.raises(LegacyFormatError, match="not a UTF-8"):
        load_legacy_grad(path)


def test_missing_file(tmp_path: Path) -> None:
    with pytest.raises(GradFileError) as info:
        load_legacy_grad(tmp_path / "нет.grad")
    assert not isinstance(info.value, LegacyFormatError)


# --- v1 time detection -------------------------------------------------------------------------------------


@pytest.mark.parametrize("fs", [2, 4, 64, 128, 500, 999])
@pytest.mark.parametrize("extra", [0, 1, -1])
def test_detects_v1_time(fs: int, extra: int) -> None:
    n = fs * 5 + (extra % fs)
    pattern = detect_v1_time(np.array(v1_time(n, fs)))
    assert pattern == V1TimePattern(sample_rate_hz=float(fs), start_second=1, repeated_tail=n % fs)


def test_detects_v1_time_with_continuing_tail() -> None:
    fs = 4
    t = [i / 1000 + j for j in range(1, 4) for i in range(fs)] + [0 / 1000 + 4, 1 / 1000 + 4]
    assert detect_v1_time(np.array(t)) == V1TimePattern(4.0, 1, 0)


@pytest.mark.parametrize("fs", [8.0, 64.0, 128.0, 1000.0])
def test_genuine_uniform_time_is_not_flagged(fs: float) -> None:
    assert detect_v1_time(np.arange(5000) / fs) is None
    assert detect_v1_time(1.0 + np.arange(5000) / fs) is None


@pytest.mark.parametrize("fs", [1, 1000])
def test_uniform_v1_rates_are_not_flagged(fs: int) -> None:
    # fs = 1 gives 1, 2, 3...; fs = 1000 gives a uniform 1 ms step: neither jumps.
    assert detect_v1_time(np.array(v1_time(fs * 4, fs))) is None


def test_near_misses_are_not_flagged() -> None:
    t = np.array(v1_time(64 * 4, 64))
    off_by_ulp = t.copy()
    off_by_ulp[100] = np.nextafter(off_by_ulp[100], np.inf)
    assert detect_v1_time(off_by_ulp) is None

    with_nan = t.copy()
    with_nan[5] = np.nan
    assert detect_v1_time(with_nan) is None

    non_uniform = np.cumsum(np.random.default_rng(1).uniform(0.001, 0.02, 500))
    assert detect_v1_time(non_uniform) is None

    assert detect_v1_time(np.array([])) is None
    assert detect_v1_time(np.array([1.0, 1.001])) is None
    assert detect_v1_time(np.array(v1_time(64, 64))) is None  # one second only: rate unknown


def test_only_the_time_column_is_checked(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"Время": v1_time(40, 8), "x": [0.0] * 40})
    result = load_legacy_grad(path)
    assert result.time_column is None
    assert result.v1_time is None
    assert result.warnings == ()


def test_genuine_time_column_gives_no_warning(tmp_path: Path) -> None:
    path = tmp_path / "a.grad"
    write_v1_grad(path, {"Time": list(np.arange(300) / 128), "x": [0.0] * 300})
    result = load_legacy_grad(path)
    assert result.time_column == "Time"
    assert result.v1_time is None
    assert result.warnings == ()


# --- real v1 files, if any ---------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path",
    LEGACY_SAMPLES or [pytest.param(None, marks=pytest.mark.skip(reason="no files in tests/data/legacy"))],
    ids=[p.name for p in LEGACY_SAMPLES] or ["none"],
)
def test_real_v1_files(path: Path) -> None:
    result = load_legacy_grad(path)
    assert FORMULAS_COLUMN not in result.data.columns
    assert all(dtype == np.float64 for dtype in result.data.dtypes)
    assert set(result.formulas) <= set(result.data.columns)
    Project(result.data, ProjectMeta(time_column=result.time_column))
