# src/ota_installer/tasks/components/base_task.py
from dataclasses import dataclass
from enum import StrEnum, auto

from ..operation.task_operation_info import TaskOperationContainer
from ..operation.task_operation_processor import TaskOperationProcessor


class OptionalTaskField(StrEnum):
    COMMAND_STRING = auto()
    COMMENT = auto()
    REMINDER = auto()


@dataclass
class BaseTask:
    """Represents a base task with associated properties."""

    def __init__(
        self,
        enum_values: TaskOperationContainer,
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

        self._find_optional_fields()

    def _find_optional_fields(self):
        for field in OptionalTaskField:
            value = getattr(self, field.value, None)
            if value is not None:
                self.task.set_item(field.value, value)
