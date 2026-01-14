# src/ota_installer/variables/constants/directory_paths.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    local_path: str
    remote_path: str
