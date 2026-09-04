# src/ota_installer/tasks/components/t10_apply_ota_update.py
from dataclasses import dataclass, field

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task.task_group.task_group_pipeline import APPLICATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = APPLICATION[1]
TITLE = STEP.name


@dataclass
class ADBSideloader(BaseTask):
    """Task to apply OTA updates using ADB sideload."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the command string for ADB sideload."""
        command_string = self._create_command_string()
        super().__init__(
            enum_values=STEP,
            command_string=command_string,
            reminder=STEP.reminder,
        )

    def _create_command_string(self) -> str:
        """Creates the command string for ADB sideload."""
        return f"adb sideload {self.instance.path}"

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB sideload task and runs it with output."""
        if self.instance.path:
            self.task.run_with_output()
        else:
            raise ValueError("No path provided for ADB sideload.")


@Plugin.TASK.register(TITLE.lower())
@dataclass
class ADBSideloaderPlugin(ADBSideloader):
    """Plugin for the ADBSideloader task."""

    pass


# Signed off by Brian Sanford on 20260626
