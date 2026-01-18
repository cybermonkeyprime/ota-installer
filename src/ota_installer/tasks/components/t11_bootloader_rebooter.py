# src/ota_installer/tasks/components/t11_bootloader_rebooter.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.REBOOT_TO_BOOTLOADER.value


@task_plugin(ApplicationTasks.REBOOT_TO_BOOTLOADER.value)
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
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.COMMAND_STRING.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished successfully!"
    )
    def perform_task(self) -> None:
        """Executes the reboot task and outputs the result."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260118
