# src/ota_installer/variables/constants/directory_paths.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class DirectoryPaths:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


# Signed off by Brian Sanford on 20260120
