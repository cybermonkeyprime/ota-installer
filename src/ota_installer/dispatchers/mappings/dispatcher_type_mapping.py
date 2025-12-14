from enum import Enum


class DispatcherTypeMapping(Enum):
    DIRECTORY = "directory"
    IMAGE = "image"
    FILE = "file"
    TASK_GROUP = "task_group"
    VARIABLE = "variable"
