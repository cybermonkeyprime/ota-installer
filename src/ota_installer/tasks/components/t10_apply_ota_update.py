# src/ota_installer/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...variables import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.APPLY_OTA_UPDATE.value


@task_plugin(ApplicationTasks.APPLY_OTA_UPDATE.value)
@dataclass
class ADBSideloader(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

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
