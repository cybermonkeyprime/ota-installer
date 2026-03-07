# src/directories/constants/magisk_paths.py
from enum import Enum
from pathlib import Path
from typing import NamedTuple


class MagiskImagePath(Enum):
    """Enumeration for Magisk image paths."""

    LOCAL_PATH = Path.home() / "Android" / "boot-images" / "magisk"
    REMOTE_PATH = Path("/sdcard") / "Download" / "magisk"

    @classmethod
    def list(cls) -> list:
        return [cls.__members__.values()]


class MagiskImageTuple(NamedTuple):
    """NamedTuple for storing Magisk image paths."""

    local_path: Path
    remote_path: Path


# Signed off by Brian Sanford on 20260305
