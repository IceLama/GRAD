from typing import TYPE_CHECKING

import numpy as np
import pytest

import grad
from grad.ui.app import main

if TYPE_CHECKING:
    from conftest import FlightDataFactory


def test_smoke(flight_data_factory: "FlightDataFactory", capsys: pytest.CaptureFixture[str]) -> None:
    # The package is installed and the entry point prints its version.
    main()
    assert capsys.readouterr().out.strip() == f"GRAD {grad.__version__}"
    assert grad.__version__ != "0+unknown"

    # The synthetic recording matches its ground truth, including non-ASCII column names.
    flight = flight_data_factory(
        fs=50.0,
        duration=20.0,
        seed=1,
        nan_gaps=[(5.0, 6.0)],
        names={"load": "Нагрузка, кН", "bridge_1": "Мост 1.T", "bridge_2": "Мост 2.T"},
    )
    data = flight.data
    t = data[flight.time].to_numpy()

    assert len(data) == 1000
    assert list(data.columns) == ["Time", "sine", "noise", "Нагрузка, кН", "Мост 1.T", "Мост 2.T"]
    np.testing.assert_allclose(np.diff(t), 1 / flight.fs)

    in_gap = (t >= 5.0) & (t < 6.0)
    measured = data.drop(columns=flight.time).to_numpy()
    assert in_gap.sum() == 50
    assert np.isnan(measured[in_gap]).all()
    assert not np.isnan(measured[~in_gap]).any()
    assert not np.isnan(t).any()

    load = data[flight.load].to_numpy()
    assert set(load[~in_gap]) == set(flight.load_levels)
    for column, truth in flight.bridges.items():
        bridge = data[column].to_numpy()
        gain, offset = np.polyfit(load[~in_gap], bridge[~in_gap], 1)
        assert gain == pytest.approx(truth.gain, rel=1e-3)
        assert offset == pytest.approx(truth.offset, abs=5 * truth.noise_std)

    bridge_1, bridge_2 = (data[c].to_numpy()[~in_gap] for c in flight.bridge_columns)
    assert abs(np.corrcoef(bridge_1, bridge_2)[0, 1]) > 0.99
