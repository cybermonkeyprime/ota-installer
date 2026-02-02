# task_groups/constants/task_group_names.py
from enum import Enum


class TaskGroupNames(Enum):
    """Enumeration for task group names."""

    PREPARATION = "preparation"
    MIGRATION = "migration"
    APPLICATION = "application"

    @property
    def lower_case(self) -> str:
        """Return the lowercase representation of the task group name."""
        return self.value.lower()

    def _value(self, obj: type) -> object:
        """Retrieve the value from the given object based on the
        task group name.
        """
        return getattr(obj, self.value)


# Signed off by Brian Sanford on 20260202
