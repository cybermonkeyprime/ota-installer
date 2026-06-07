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
        self._set_required_fields()
        self._set_optional_fields()

    def _set_required_fields(self) -> None:
        required_fields = ("index", "title", "description")
        for field in required_fields:
            self.task.set_item(field, getattr(self.enum_values, field))

    def _set_optional_fields(self) -> None:
        for field in OptionalTaskField:
            value = getattr(self, field.name.lower(), None)
            if value is not None:
                self.task.set_item(field.name.lower(), value)
