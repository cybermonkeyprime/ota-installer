# validation/task_group_validator.py
from ..task_groups.constants.task_group_names import TaskGroupNames


def validate_task_group(value: str) -> bool:
    """Validate the provided task group name."""
    return TaskGroupNames[value.upper()].validation
