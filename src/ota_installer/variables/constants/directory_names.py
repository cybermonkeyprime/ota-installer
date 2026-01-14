# src/ota_installer/variables/constants/directories.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DirectoryNames(object):
    magisk: dict
