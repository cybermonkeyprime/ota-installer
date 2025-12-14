# src/tasks/components/04_stock_boot_image_backuppper.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails
from src.tasks.task_operation_processor import (
    image_handler,
)

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BACKUP_STOCK_BOOT_IMAGE.value


@dataclass
class StockBootImageBackupper(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        image_path = image_handler(self.instance.file_name["device"])
        command_string = (
            f"cp -v {image_path} {self.instance.file_paths['stock']}"
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
