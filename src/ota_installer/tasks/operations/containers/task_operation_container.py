# src/ota_installer/tasks/operations/containers/task_operation_container.py
from dataclasses import dataclass


@dataclass
class TaskOperationContainer:
    """Container for task operation details."""

    index: int
    title: str
    description: str
    command_string: str | None = None
    reminder: str | None = None


# Signed off by Brian Sanford on 20260209
