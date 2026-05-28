# src/ota_installer/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...handler.task_group_handler import PreparationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "RENAME_PAYLOAD_IMAGE"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


@task_plugin(PreparationTask[TITLE].value)
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

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Executes the task to rename the payload image."""
        self.task.run_with_output()
