# src/ota_installer/variables/constants/file_names.py
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileNameInfo(object):
    path: Path
    stem: str
    parts: Callable
    device: str
    version: str
