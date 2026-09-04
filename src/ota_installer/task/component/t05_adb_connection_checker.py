# src/ota_installer/tasks/components/t05_adb_connection_checker.py
from dataclasses import dataclass, field

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task.task_group.task_group_pipeline import MIGRATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = MIGRATION[0]
TITLE = STEP.name


@dataclass
class ADBConnectionChecker(BaseTask):
    """Checks the ADB connection status and performs the task."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the ADBConnectionChecker with command string."""
        super().__init__(
            enum_values=STEP,
            command_string=STEP.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB connection check task."""
        self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class ADBConnectionCheckerPlugin(ADBConnectionChecker):
    """Plugin for the ADBConnectionChecker task."""

    pass


# Signed off by Brian Sanford on 20260625
