# src/ota_installer/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

from ota_installer.task.task_info import TaskID

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import PreparationTask
from ...variable.variable_manager import VariableManager
from .base_task import BaseTask

TITLE = TaskID.RENAME_PAYLOAD_IMAGE


@dataclass
class PayloadImageRenamer(BaseTask):
    """Renames the payload image file to a specified path."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for renaming the payload image."""

        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=self._create_rename_command(),
        )

    def _create_rename_command(self) -> str:
        """Generates the command string for renaming the payload image."""
        source_path = Path.home() / "payload.bin"
        destination_path = self.instance.file_paths.payload
        return f"mv -v {source_path} {destination_path}"

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to rename the payload image."""
        self.task.run_with_output()


@task_plugin(PreparationTask[TITLE.name].value)
@dataclass
class PayloadImageRenamerPlugin(PayloadImageRenamer):
    """Plugin for the PayloadImageRenamer task."""

    pass


# Signed off by Brian Sanford on 20260528
