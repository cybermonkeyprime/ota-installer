# src/ota_installer/variables/constants/directory_paths.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    local_path: Path
    remote_path: Path
