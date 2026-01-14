# src/ota_installer/variables/constants/file_paths.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FilePaths(object):
    stock: str
    magisk: str
    payload: str
    log_file: str
