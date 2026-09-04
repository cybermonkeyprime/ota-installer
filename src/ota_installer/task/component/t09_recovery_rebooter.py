# src/ota_installer/tasks/components/t09_recovery_rebooter.py
from dataclasses import dataclass, field

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task.task_group.task_group_pipeline import APPLICATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = APPLICATION[0]
TITLE = STEP.name


@dataclass
class RecoveryRebooter(BaseTask):
    """Task to reboot the system into recovery mode."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        super().__init__(
            enum_values=STEP,
            command_string=STEP.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the task to reboot into recovery mode."""
        if self.task:
            self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class RecoveryRebooterPlugin(RecoveryRebooter):
    """Plugin for the RecoveryRebooter task."""

    pass


# Signed off by Brian Sanford on 20260625
