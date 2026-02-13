# src/ota_installer/variables/constants/file_paths.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FilePaths(object):
    """Container for file paths used in the OTA installer."""

    stock: Path
    magisk: Path
    payload: Path
    log_file: str


# Signed off by Brian Sanford on 20260213
