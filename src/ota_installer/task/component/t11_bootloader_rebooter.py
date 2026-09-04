# src/ota_installer/tasks/components/t11_bootloader_rebooter.py
from dataclasses import dataclass, field

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...variable.variable_director import VariableDirector
from ...task.task_group.task_group_pipeline import APPLICATION
from .base_task import BaseTask

STEP = APPLICATION[2]
TITLE = STEP.name


@dataclass
class BootloaderRebooter(BaseTask):
    """Handles the rebooting process to the bootloader."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the BootloaderRebooter with command string."""
        super().__init__(
            enum_values=STEP,
            command_string=STEP.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the reboot task and outputs the result."""
        self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class BootloaderRebooterPlugin(BootloaderRebooter):
    """Plugin for the BootloaderRebooter task."""

    pass


# Signed off by Brian Sanford on 20260626
