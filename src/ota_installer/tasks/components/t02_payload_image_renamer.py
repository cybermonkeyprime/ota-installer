# src/ota_installer/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.RENAME_PAYLOAD_IMAGE.value


@task_plugin(PreparationTasks.RENAME_PAYLOAD_IMAGE.value)
@dataclass
class PayloadImageRenamer(BaseTask):
    """Renames the payload image file to a specified path."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for renaming the payload image."""

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=self._create_rename_command(),
        )

    def _create_rename_command(self) -> str:
        """Generates the command string for renaming the payload image."""
        source_path = Path.home() / "payload.bin"
        destination_path = self.instance.file_paths.payload
        return f"mv -v {source_path} {destination_path}"

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to rename the payload image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260203
