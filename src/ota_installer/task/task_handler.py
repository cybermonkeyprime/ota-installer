# src/ota_installer/handler/task_handler.py
from dataclasses import dataclass
from enum import Enum

from ota_installer.task import task_group_handler

from .. import decorator
from ..task.task_group_handler import (
    ApplicationTask,
    MigrationTask,
    PreparationTask,
    TaskGroupName,
)


@dataclass(frozen=True)
class TaskDefinitionContainer:
    """
    Handles the definitions of various task categories and their UI rendering.
    """

    _class: type
    _name: str

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Executes the task's generation logic wrapped in the required UI
            decorators.
        """

        # 1. This encapsulates your internal execution context
        def result():
            return self._class.get_member_names()

        # 2. Define the execution closure and apply your outer decorator
        @decorator.PaddedFooterWrapper()
        def execute_pipeline():
            # Apply your dynamic inner decorator
            decorated_function = decorator.ConfirmationPrompt(
                char=" ", comment=f"perform the {self._name}s"
            )(result)

            return decorated_function()

        # 3. Fire the pipeline and hand back the final tuple payload
        return execute_pipeline()


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


TASK_DEFINITION_MAPPING = {
    TaskGroupName.PREPARATION.value: TaskDefinitionContainer(
        PreparationTask, "Preparation Task"
    ),
    TaskGroupName.MIGRATION.value: TaskDefinitionContainer(
        MigrationTask, "Migration Task"
    ),
    TaskGroupName.APPLICATION.value: TaskDefinitionContainer(
        ApplicationTask, "Application Task"
    ),
}

# Signed off by Brian Sanford on 20260523
