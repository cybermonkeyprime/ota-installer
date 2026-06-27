# src/ota_installer/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import ApplicationTask
from ...variable.variable_manager import VariableManager
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.APPLY_OTA_UPDATE


@dataclass
class ADBSideloader(BaseTask):
    """Task to apply OTA updates using ADB sideload."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for ADB sideload."""
        command_string = self._create_command_string()
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=command_string,
            reminder=TITLE.enum_values.reminder,
        )

    def _create_command_string(self) -> str:
        """Creates the command string for ADB sideload."""
        return f"adb sideload {self.instance.path}"

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB sideload task and runs it with output."""
        if self.instance.path:
            self.task.run_with_output()
        else:
            raise ValueError("No path provided for ADB sideload.")


@task_plugin(ApplicationTask[TITLE.name].value)
@dataclass
class ADBSideloaderPlugin(ADBSideloader):
    """Plugin for the ADBSideloader task."""

    pass


# Signed off by Brian Sanford on 20260626
