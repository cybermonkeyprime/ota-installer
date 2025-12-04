from enum import Enum


class TaskGroupTypeMapping(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    def _value(self, obj: type) -> object:
        return getattr(obj, self.value)
