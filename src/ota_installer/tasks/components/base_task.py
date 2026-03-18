# src/ota_installer/tasks/components/base_task.py
from dataclasses import dataclass
from enum import StrEnum, auto

from ..operations.task_operation_details import TaskOperation
from ..operations.task_operation_processor import TaskOperationProcessor


class OptionalTaskField(StrEnum):
    COMMAND_STRING = auto()
    COMMENT = auto()
    REMINDER = auto()


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

        for attr in OptionalTaskField:
            if value := getattr(self, attr, None):
                self.task.set_item(attr, value)


