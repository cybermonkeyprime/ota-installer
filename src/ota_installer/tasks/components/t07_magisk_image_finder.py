# src/ota_installer/tasks/components/t07_magisk_image_finder.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.migration_tasks import MigrationTasks
from ...variables import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.FIND_MAGISK_IMAGE.value


@task_plugin(MigrationTasks.FIND_PATCHED_BOOT_IMAGE.task_name)
@dataclass
class MagiskImageFinder(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        command_string = (
            f'adb shell ls "{self.instance.directories["magisk"]["remote_path"]}"'
            "| grep magisk_patched | head -n1"
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
