# src/ota_installer/variables/constants/directories.py
from dataclasses import dataclass

from .directory_paths import DirectoryPaths


@dataclass(frozen=True, slots=True)
class DirectoryNames(object):
    magisk: DirectoryPaths
