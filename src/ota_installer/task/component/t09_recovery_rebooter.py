# src/ota_installer/tasks/components/t09_recovery_rebooter.py
from dataclasses import dataclass, field

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task_group.task_group_handler import ApplicationTask
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.REBOOT_TO_RECOVERY.value


@dataclass
class RecoveryRebooter(BaseTask):
    """Task to reboot the system into recovery mode."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to reboot into recovery mode."""
        self.task.run_with_output()


@task_plugin(ApplicationTask.REBOOT_TO_RECOVERY.value)
@dataclass
class RecoveryRebooterPlugin(RecoveryRebooter):
    """Plugin for the RecoveryRebooter task."""

    pass
