# src/ota_installer/handler/task_handler.py
from dataclasses import dataclass

from .. import decorator
from ..task.task_group_handler import (
    ApplicationTask,
    MigrationTask,
    PreparationTask,
    TaskGroupName,
)


@dataclass(frozen=True)
class TaskDefinitionRenderer:
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


TASK_DEFINITION_MAPPING = {
    TaskGroupName.PREPARATION.value: TaskDefinitionRenderer(
        PreparationTask, "Preparation Task"
    ),
    TaskGroupName.MIGRATION.value: TaskDefinitionRenderer(
        MigrationTask, "Migration Task"
    ),
    TaskGroupName.APPLICATION.value: TaskDefinitionRenderer(
        ApplicationTask, "Application Task"
    ),
}

# Signed off by Brian Sanford on 20260523
