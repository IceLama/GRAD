"""Exceptions raised by GRAD core.

Every error core reports to the user is a `GradError` subclass. Messages are plain English sentences that
name the file, parameter or value at fault; the UI may show them as is or map the exception type (and its
attributes) to localized text.
"""

import os
from pathlib import Path


class GradError(Exception):
    """Base class for all errors core reports to the user."""


class ProjectValidationError(GradError):
    """Project data or metadata breaks an invariant (wrong dtype, duplicate name, unknown time column...)."""


class TimeBaseError(GradError):
    """The project has neither a time column nor a sample rate, so time cannot be computed."""


class GradFileError(GradError):
    """A file could not be read or written: missing, no permission, disk full and the like."""

    def __init__(self, message: str, path: str | os.PathLike[str]) -> None:
        super().__init__(message)
        self.path = Path(path)


class ProjectFileError(GradFileError):
    """A `.gradproj` file is damaged or does not follow the project file format."""


class UnsupportedVersionError(ProjectFileError):
    """A `.gradproj` file was written by a newer GRAD with a schema this version cannot read."""

    def __init__(self, path: str | os.PathLike[str], found: int, supported: int) -> None:
        super().__init__(
            f"Project file {Path(path).name} has schema version {found}, but this GRAD reads versions up to "
            f"{supported}. Open it with a newer GRAD.",
            path,
        )
        self.found = found
        self.supported = supported


class LegacyFormatError(GradFileError):
    """A GRAD v1 `.grad` file cannot be read: bad header, non-numeric value, wrong encoding..."""

    def __init__(
        self,
        message: str,
        path: str | os.PathLike[str],
        *,
        column: str | None = None,
        line: int | None = None,
    ) -> None:
        super().__init__(message, path)
        self.column = column
        self.line = line
