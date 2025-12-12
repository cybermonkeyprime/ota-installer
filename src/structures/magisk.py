# src/structures/magisk.py
from dataclasses import dataclass, field
from pathlib import Path

from src.paths.constants import MagiskImagePaths


@dataclass
class MagiskStruct(object):
    local_path: Path = field(
        default_factory=lambda: MagiskImagePaths.LOCAL_PATH.value
    )
    remote_path: Path = field(
        default_factory=lambda: MagiskImagePaths.REMOTE_PATH.value
    )
