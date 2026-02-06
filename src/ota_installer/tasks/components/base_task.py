# src/ota_installer/tasks/components/base_task.py
from dataclasses import dataclass

from ..operations.task_operation_details import TaskOperation
from ..operations.task_operation_processor import TaskOperationProcessor


@dataclass
class BaseTask(object):
    """Represents a base task with associated properties."""

    def __init__(
        self,
        enum_values: TaskOperation,
        command_string: str | None = None,
        comment: str | None = None,
        reminder: str | None = None,
    ):
        """Initializes the task operation processor with task details."""
        self.enum_values = enum_values
        self.command_string = command_string
        self.comment = comment
        self.reminder = reminder
        self.task = TaskOperationProcessor()
        self._initialize_task()

    def _initialize_task(self) -> None:
        """
        Sets the task items based on the provided enum values and optional
        parameters.
        """
        self.task.set_item("index", self.enum_values.index)
        self.task.set_item("title", self.enum_values.title)
        self.task.set_item("description", self.enum_values.description)

        if self.command_string:
            self.task.set_item("command_string", self.command_string)
        if self.comment:
            self.task.set_item("comment", self.comment)
        if self.reminder:
            self.task.set_item("reminder", self.reminder)


# Signed off by Brian Sanford on 20260202
