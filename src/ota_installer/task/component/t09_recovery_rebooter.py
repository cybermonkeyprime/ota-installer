# src/ota_installer/tasks/components/t09_recovery_rebooter.py
from dataclasses import dataclass, field

from ... import decorator
from ...handler.task_group_handler import ApplicationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "REBOOT_TO_RECOVERY"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


@dataclass
class RecoveryRebooter(BaseTask):
    """Task to reboot the system into recovery mode."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Executes the task to reboot into recovery mode."""
        self.task.run_with_output()


@task_plugin(ApplicationTask[TITLE].value)
@dataclass
class RecoveryRebooterPlugin(RecoveryRebooter):
    """Plugin for the RecoveryRebooter task."""

    pass
