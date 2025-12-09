# src/variables/constants.py
from enum import Enum


class DispatcherTypes(Enum):
    DIRECTORY = "directory"
    FILE = "file"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return self.value
