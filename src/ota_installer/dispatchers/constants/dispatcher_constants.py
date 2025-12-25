# src/ota_installer/dispatchers/constants/dispatcher_constants.py
from enum import Enum


class DispatcherConstants(Enum):
    DIRECTORY = "directory"
    IMAGE = "image"
    FILE = "file"
    TASK_GROUP = "task_group"
    VARIABLE = "variable"
