# src/ota_installer/handler/task_handler.py
from dataclasses import dataclass
from enum import Enum

from .. import decorator
from ..task.task_group_handler import (
    ApplicationTask,
    MigrationTask,
    PreparationTask,
    TaskGroupName,
)


@dataclass(frozen=True)
class TaskDefinitionContainer:
    """Handles the definitions of various task categories."""

    _class: type
    _name: str


class TaskDefinitionInfo(Enum):
    PREPARATION = TaskDefinitionContainer(PreparationTask, "Preparation Task")
    MIGRATION = TaskDefinitionContainer(MigrationTask, "Migration Task")
    APPLICATION = TaskDefinitionContainer(ApplicationTask, "Application Task")

    @property
    def task_class(self) -> type:
        return self.value._class

    @property
    def display_name(self) -> str:
        return self.value._name

    @decorator.PaddedFooterWrapper()
    def render(self) -> tuple:
        def result():
            return self.get_definitions(self.task_class)

        decorated_function = decorator.ConfirmationPrompt(
            char=" ", comment=f"perform the {self.display_name}s"
        )(result)  # type: ignore[reportArgumentType]

        return decorated_function()

    def get_definitions(self, task_class) -> tuple:
        """Helper method to get task definitions from a task class."""
        return task_class.get_member_names()


# Signed off by Brian Sanford on 20260523
