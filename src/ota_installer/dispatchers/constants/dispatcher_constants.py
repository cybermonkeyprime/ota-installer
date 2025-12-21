# src/ota_installer/dispatchers/constants/dispatcher_type_constants.py
from enum import Enum


class DispatcherTypeConstants(Enum):
    DIRECTORY = "directory"
    IMAGE = "image"
    FILE = "file"
    TASK_GROUP = "task_group"
    VARIABLE = "variable"
