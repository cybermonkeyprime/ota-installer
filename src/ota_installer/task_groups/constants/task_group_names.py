from enum import Enum


class TaskGroupTypeConstants(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    def _value(self, obj: type) -> object:
        return getattr(obj, self.value)


class TaskGroups(Enum):
    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    @property
    def lower_case(self) -> str:
        return self.value.lower()
