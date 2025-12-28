# src/ota_installer/dispatchers/constants/dispatcher_constants.py
from enum import StrEnum, auto


class DispatcherConstants(StrEnum):
    DIRECTORY = auto()
    IMAGE = auto()
    FILE = auto()
    TASK_GROUP = auto()
    VARIABLE = auto()
