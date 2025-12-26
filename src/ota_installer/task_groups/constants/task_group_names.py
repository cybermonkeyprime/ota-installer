# task_groups/constants/task_group_names.py
from enum import Enum


class TaskGroupNames(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    @property
    def lower_case(self) -> str:
        return self.value.lower()

    def _value(self, obj: type) -> object:
        return getattr(obj, self.value)
