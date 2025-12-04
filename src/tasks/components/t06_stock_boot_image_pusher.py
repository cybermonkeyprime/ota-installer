# src/tasks/components/t06_stock_boot_image_pusher.py
from dataclasses import dataclass, field
from pathlib import Path

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PUSH_STOCK_BOOT_IMAGE.value


@dataclass
class StockBootImagePusher(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        stock_image = self.instance.boot_image_struct.stock
        stock_path = (
            Path.home() / stock_image.directory_path / stock_image.file_name
        )
        command_string = f'adb push "{stock_path}" /sdcard/'

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
            reminder=ENUM_VALUES.REMINDER.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
