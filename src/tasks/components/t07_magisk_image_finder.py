# src/tasks/components/t07_magisk_image_finder.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.FIND_MAGISK_IMAGE.value


@dataclass
class MagiskImageFinder(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        remote_path = self.instance.directory.magisk_image.remote_path
        command_string = (
            f'adb shell ls "{remote_path}" | grep magisk_patched | head -n1'
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.show_index_and_title()
        if getattr(self.task, "description", None):
            self.task.show_description()

        result = self.task.execute_and_return_output("Patched Boot Image")
        if result:
            self.instance.patched_image_name = result
        if getattr(self.task, "reminder", None):
            self.task.show_reminder()
