# src/ota_installer/variables/constants/file_paths.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FilePaths(object):
    stock: Path
    magisk: Path
    payload: Path
    log_file: str
