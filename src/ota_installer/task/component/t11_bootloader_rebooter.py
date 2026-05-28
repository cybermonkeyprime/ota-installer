# src/ota_installer/tasks/components/t11_bootloader_rebooter.py
from dataclasses import dataclass, field

from ... import decorator
from ...handler.task_group_handler import ApplicationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "REBOOT_TO_BOOTLOADER"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


@dataclass
class BootloaderRebooter(BaseTask):
    """Handles the rebooting process to the bootloader.

    This task is responsible for executing the command to reboot
    the system into the bootloader mode and providing feedback
    upon completion.
    """

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the BootloaderRebooter with command string."""
        super().__init__(
            enum_values=ENUM_VALUES, command_string=ENUM_VALUES.command_string
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Executes the reboot task and outputs the result."""
        self.task.run_with_output()


@task_plugin(ApplicationTask[TITLE].value)
@dataclass
class BootloaderRebooterPlugin(BootloaderRebooter):
    """Plugin for the RecoveryRebooter task."""

    pass
