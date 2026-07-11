# src/ota_installer/tasks/components/t11_bootloader_rebooter.py
from dataclasses import dataclass, field

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import ApplicationTask
from ...variable.variable_director import VariableDirector
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.REBOOT_TO_BOOTLOADER


@dataclass
class BootloaderRebooter(BaseTask):
    """Handles the rebooting process to the bootloader."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the BootloaderRebooter with command string."""
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=TITLE.enum_values.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the reboot task and outputs the result."""
        self.task.run_with_output()


@task_plugin(ApplicationTask[TITLE.name].value)
@dataclass
class BootloaderRebooterPlugin(BootloaderRebooter):
    """Plugin for the BootloaderRebooter task."""

    pass


# Signed off by Brian Sanford on 20260626
