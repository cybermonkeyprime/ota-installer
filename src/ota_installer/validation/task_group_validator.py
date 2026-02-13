# validation/task_group_validator.py
from ..task_groups.constants.task_group_names import TaskGroupNames


def validate_task_group(value: str) -> TaskGroupNames:
    """Validate the provided task group name."""
    return TaskGroupNames[value.upper()] or None


# Signed off by Brian Sanford on 20260213
