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
        command_string = (
            f'adb shell ls "{remote_path}"| grep magisk_patched | head -n1'
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.show_index_and_title()
        if getattr(self.task, "description", None):
            self.task.show_description()

        result = self.task.execute_and_return_output("Patched Boot Image")
        if result:
            self.instance.image_name["patched"] = result
        if getattr(self.task, "reminder", None):
            self.task.show_reminder()
