# src/ota_installer/task_group/task_group_names.py
from enum import StrEnum, auto


class TaskGroupName(StrEnum):
    """Enumeration for task group names."""

    PREPARATION = auto()
    MIGRATION = auto()
    APPLICATION = auto()

    @classmethod
    def get_task_group_members(cls) -> tuple[str, ...]:
        """Returns the keys of the task groups."""
        return tuple(enum.value for enum in cls)


# Signed off by Brian Sanford on 20260903
