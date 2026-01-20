# src/ota_installer/variables/constants/file_names.py
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileNameInfo(object):
    """Represents information about a file name."""

    path: Path
    stem: str
    parts: Callable
    device: str
    version: str


# Signed off by Brian Sanford on 20260120
