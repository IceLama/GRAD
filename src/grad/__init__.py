"""GRAD: flight-test data processing and strain-gauge calibration."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("grad")
except PackageNotFoundError:  # running from a source tree without installation
    __version__ = "0+unknown"
