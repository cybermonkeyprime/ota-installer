# src/ota_installer/task_groups/containers/taskgroup_container.py
from typing import NamedTuple


class TaskGroupContainer(NamedTuple):
    """Container for task group information."""

    group_name: str
    group_enum: str | None


# Signed off by Brian Sanford on 20260129
