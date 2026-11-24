"""Shared pytest fixtures.

`flight_data_factory` builds synthetic flight-test recordings with known ground truth, so tests can check
loaders, the pipeline and the regression against exact expected values.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest

#: Canonical channel keys, in column order. Use `names=` to give them other column names.
CHANNELS: tuple[str, ...] = ("time", "sine", "noise", "load", "bridge_1", "bridge_2")

DEFAULT_NAMES: Mapping[str, str] = MappingProxyType(
    {
        "time": "Time",
        "sine": "sine",
        "noise": "noise",
        "load": "load",
        "bridge_1": "bridge_1",
        "bridge_2": "bridge_2",
    }
)


@dataclass(frozen=True)
class BridgeTruth:
    """Ground truth of a synthetic strain-bridge channel: `bridge = gain * load + offset + noise`."""

    gain: float
    offset: float
    noise_std: float


@dataclass(frozen=True)
class SyntheticFlight:
    """A synthetic recording and the parameters it was generated from."""

    data: pd.DataFrame
    fs: float
    names: Mapping[str, str]
    """Canonical channel key -> column name in `data`."""
    load_levels: tuple[float, ...]
    bridges: Mapping[str, BridgeTruth]
    """Bridge column name -> ground truth."""
    sine_hz: float
    sine_amplitude: float
    nan_gaps: tuple[tuple[float, float], ...] = field(default=())

    @property
    def time(self) -> str:
        return self.names["time"]

    @property
    def load(self) -> str:
        return self.names["load"]

    @property
    def bridge_columns(self) -> tuple[str, str]:
        return self.names["bridge_1"], self.names["bridge_2"]


def make_synthetic_flight(
    *,
    fs: float = 64.0,
    duration: float = 60.0,
    t0: float = 0.0,
    seed: int = 0,
    sine_hz: float = 1.0,
    sine_amplitude: float = 1.0,
    noise_std: float = 1.0,
    load_levels: Sequence[float] = (0.0, 250.0, 500.0, 750.0, 1000.0, 500.0, 0.0),
    bridge_gains: tuple[float, float] = (2.0e-3, -1.5e-3),
    bridge_offsets: tuple[float, float] = (0.05, -0.02),
    bridge_noise_std: float = 0.01,
    nan_gaps: Sequence[tuple[float, float]] = (),
    nan_channels: Sequence[str] | None = None,
    names: Mapping[str, str] | None = None,
) -> SyntheticFlight:
    """Build a synthetic flight recording.

    - Time is uniform: `t0 + i / fs` for `i in range(round(duration * fs))`.
    - `sine`: `sine_amplitude * sin(2*pi*sine_hz*t)`; `noise`: Gaussian with `noise_std`.
    - `load`: stepwise, the samples split into `len(load_levels)` equal plateaus, noise-free.
    - `bridge_k = bridge_gains[k] * load + bridge_offsets[k] + N(0, bridge_noise_std)`, so both bridges
      are correlated through the load.
    - `nan_gaps`: half-open time ranges `[start, end)` set to NaN in `nan_channels`
      (canonical keys; default: every channel except time).
    - `names`: canonical key -> column name overrides, e.g. Cyrillic names or names with dots and spaces.
    """
    if fs <= 0:
        raise ValueError(f"fs must be positive, got {fs}")
    if duration < 0:
        raise ValueError(f"duration must be non-negative, got {duration}")
    if not 0 < sine_hz < fs / 2:
        raise ValueError(f"sine_hz must be in (0, fs/2) = (0, {fs / 2}), got {sine_hz}")
    if not load_levels:
        raise ValueError("load_levels must not be empty")
    for start, end in nan_gaps:
        if not start < end:
            raise ValueError(f"NaN gap must have start < end, got ({start}, {end})")

    column_names = dict(DEFAULT_NAMES)
    if names:
        unknown = set(names) - set(CHANNELS)
        if unknown:
            raise ValueError(f"Unknown channel keys in names: {sorted(unknown)}")
        column_names.update(names)
    if len(set(column_names.values())) != len(CHANNELS):
        raise ValueError(f"Column names must be unique, got {column_names}")

    gap_channels = [c for c in CHANNELS if c != "time"] if nan_channels is None else list(nan_channels)
    unknown = set(gap_channels) - set(CHANNELS)
    if unknown:
        raise ValueError(f"Unknown channel keys in nan_channels: {sorted(unknown)}")

    rng = np.random.default_rng(seed)
    n = round(duration * fs)
    time = t0 + np.arange(n, dtype=np.float64) / fs

    load = np.empty(n, dtype=np.float64)
    for level, idx in zip(load_levels, np.array_split(np.arange(n), len(load_levels)), strict=True):
        load[idx] = level

    channels: dict[str, np.ndarray] = {
        "time": time,
        "sine": sine_amplitude * np.sin(2 * np.pi * sine_hz * time),
        "noise": rng.normal(0.0, noise_std, n),
        "load": load,
    }
    bridges: dict[str, BridgeTruth] = {}
    for k, (gain, offset) in enumerate(zip(bridge_gains, bridge_offsets, strict=True), start=1):
        key = f"bridge_{k}"
        channels[key] = gain * load + offset + rng.normal(0.0, bridge_noise_std, n)
        bridges[column_names[key]] = BridgeTruth(gain=gain, offset=offset, noise_std=bridge_noise_std)

    if nan_gaps:
        in_gap = np.zeros(n, dtype=bool)
        for start, end in nan_gaps:
            in_gap |= (time >= start) & (time < end)
        for key in gap_channels:
            channels[key] = np.where(in_gap, np.nan, channels[key])

    data = pd.DataFrame({column_names[key]: channels[key] for key in CHANNELS})
    return SyntheticFlight(
        data=data,
        fs=fs,
        names=MappingProxyType(column_names),
        load_levels=tuple(load_levels),
        bridges=MappingProxyType(bridges),
        sine_hz=sine_hz,
        sine_amplitude=sine_amplitude,
        nan_gaps=tuple(nan_gaps),
    )


FlightDataFactory = Callable[..., SyntheticFlight]


@pytest.fixture
def flight_data_factory() -> FlightDataFactory:
    """Return `make_synthetic_flight`; call it with keyword arguments to build a recording."""
    return make_synthetic_flight
