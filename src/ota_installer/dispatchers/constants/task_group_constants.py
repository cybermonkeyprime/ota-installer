# src/ota_installer/dispatchers/constants/task_group_type_constants.py
from collections import namedtuple
from enum import Enum

TaskGroupData = namedtuple("TaskGroupData", ["name", "task_enum"])


class TaskGroupTypeConstants(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    def _value(self, obj: type) -> object:
        return getattr(obj, self.value)


class PreparationTasks(Enum):
    pass


class TaskConstants(Enum):
    PREPARATION = TaskGroupData("preparation", PreparationTasks)
    MIGRATION = "migration"
    APPLICATION = "application"
