# src/tasks/components/t12_magisk_image_booter.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails
from src.tasks.task_operation_processor import image_handler

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BOOT_TO_MAGISK_IMAGE.value


@dataclass
class MagiskImageBooter(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        magisk = self.instance.boot_image_paths.magisk
        device = self.instance.file_name_parser.device
        partition = image_handler(device).stem
        command_string = f"fastboot flash {partition} {magisk}"

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
