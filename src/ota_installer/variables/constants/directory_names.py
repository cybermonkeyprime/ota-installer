# src/ota_installer/variables/constants/directories.py
from dataclasses import dataclass

from .directory_paths import DirectoryPaths


@dataclass(frozen=True, slots=True)
class DirectoryNames(object):
    """Container for directory names used in the OTA installer."""

    magisk: DirectoryPaths


# Signed off by Brian Sanford on 20260120
