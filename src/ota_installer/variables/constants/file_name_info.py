# src/ota_installer/variables/constants/file_names.py
from dataclasses import dataclass
from pathlib import Path

from ota_installer.variables.containers.file_name_container import (
    FileNameContainer,
)


@dataclass(frozen=True, slots=True)
class FileNameInfo(object):
    """Represents information about a file name."""

    path: Path
    stem: str
    parts: FileNameContainer
    device: str
    version: str


# Signed off by Brian Sanford on 20260213
