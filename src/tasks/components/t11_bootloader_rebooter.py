# src/tasks/components/t11_bootloader_rebooter.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.REBOOT_TO_BOOTLOADER.value


@dataclass
class BootloaderRebooter(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.COMMAND_STRING.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
