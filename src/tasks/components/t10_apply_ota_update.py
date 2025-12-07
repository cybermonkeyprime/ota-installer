# src/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.APPLY_OTA_UPDATE.value


@dataclass
class ADBSideloader(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        command_string = f"adb sideload {self.instance.path}"
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
            reminder=ENUM_VALUES.REMINDER.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
