# src/ota_installer/tasks/components/t09_recovery_rebooter.py
from dataclasses import dataclass, field

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_handler import ApplicationTask
from ...variable.variable_manager import VariableManager
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.REBOOT_TO_RECOVERY


@dataclass
class RecoveryRebooter(BaseTask):
    """Task to reboot the system into recovery mode."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=TITLE.enum_values.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to reboot into recovery mode."""
        if self.task:
            self.task.run_with_output()


@task_plugin(ApplicationTask[TITLE.name].value)
@dataclass
class RecoveryRebooterPlugin(RecoveryRebooter):
    """Plugin for the RecoveryRebooter task."""

    pass


# Signed off by Brian Sanford on 20260607
