# src/ota_installer/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

from ... import decorator
from ...handler.task_group_handler import ApplicationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "APPLY_OTA_UPDATE"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


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

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB sideload task and runs it with output."""
        self.task.run_with_output()


@task_plugin(ApplicationTask[TITLE].value)
@dataclass
class ADBSideloaderPlugin(ADBSideloader):
    """Plugin for the RecoveryRebooter task."""

    pass


# Signed off by Brian Sanford on 20260527
