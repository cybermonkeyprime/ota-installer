# src/ota_installer/tasks/components/t07_magisk_image_finder.py
from dataclasses import dataclass, field

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
        remote_path = "{self.instance.directories.magisk.remote_path}"
        command_string = self._build_command_string(remote_path)

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    def _build_command_string(self, remote_path: str) -> str:
        """Builds the command string to find the patched boot image."""
        return f'adb shell ls "{remote_path}" | grep magisk_patched | head -n1'

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Performs the task of finding the patched boot image."""
        self.task.show_index_and_title()
        if getattr(self.task, "description", None):
            self.task.show_description()

        result = self.task.execute_and_return_output("Patched Boot Image")
        if result:
            self.instance.image_name["patched"] = result
        if getattr(self.task, "reminder", None):
            self.task.show_reminder()


# Signed off by Brian Sanford on 20260119
