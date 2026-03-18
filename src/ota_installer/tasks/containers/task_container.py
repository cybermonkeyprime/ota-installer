# src/ota_installer/tasks/containers/task_container.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TaskContainer(object):
    """Container for task information."""

    task_name: str
    task_class: type


# Final sign off by Brian Sanford on 20260318
