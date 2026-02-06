# src/ota_installer/tasks/components/t07_magisk_image_finder.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.migration_task import MigrationTask
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.FIND_MAGISK_IMAGE.value


@task_plugin(MigrationTask.FIND_PATCHED_BOOT_IMAGE.value)
@dataclass
class MagiskImageFinder(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        remote_path = Path(self.instance.directories.magisk.remote_path)
        command_string = self._create_command_string(remote_path)
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    def _create_command_string(self, remote_path: Path) -> str:
        """Constructs the command string to locate the patched boot image."""
        return f"adb shell ls {remote_path} | grep magisk_patched | head -n1"

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task of locating the patched boot image."""
        self.task.show_index_and_title()
        if getattr(self.task, "description", None):
            self.task.show_description()

        result = self.task.execute_and_return_output("Patched Boot Image")
        if result:
            self.instance.image_name["patched"] = result
        if getattr(self.task, "reminder", None):
            self.task.show_reminder()


# Signed off by Brian Sanford on 20260202
