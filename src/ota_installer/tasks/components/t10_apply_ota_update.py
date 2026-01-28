# src/ota_installer/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.APPLY_OTA_UPDATE.value


@task_plugin(ApplicationTasks.APPLY_OTA_UPDATE.value)
@dataclass
class ADBSideloader(BaseTask):
    """Task to apply OTA updates using ADB sideload."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for ADB sideload."""
        command_string = self._create_command_string()
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
            reminder=ENUM_VALUES.reminder,
        )

    def _create_command_string(self) -> str:
        """Creates the command string for ADB sideload."""
        return f"adb sideload {self.instance.path}"

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished successfully!"
    )
    def perform_task(self) -> None:
        """Executes the ADB sideload task and runs it with output."""
        self.task.run_with_output()


