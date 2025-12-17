# src/ota_installer/tasks/components/t09_recovery_rebooter.py
from dataclasses import dataclass, field

from ... import decorators
from ...variables import VariableManager
from ..mappings.constants import ApplicationTasks
from ..plugin_registry import task_plugin
from ..task_operation_details import TaskOperationDetails
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.REBOOT_TO_RECOVERY.value


@task_plugin(ApplicationTasks.REBOOT_TO_RECOVERY.value)
@dataclass
class RecoveryRebooter(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.COMMAND_STRING.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
