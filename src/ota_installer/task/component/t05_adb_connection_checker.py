# src/ota_installer/tasks/components/t05_adb_connection_checker.py
from dataclasses import dataclass, field

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import MigrationTask
from ...variable.variable_director import VariableDirector
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.CHECK_ADB_CONNECTION


@dataclass
class ADBConnectionChecker(BaseTask):
    """Checks the ADB connection status and performs the task."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the ADBConnectionChecker with command string."""
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=TITLE.enum_values.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB connection check task."""
        self.task.run_with_output()


@task_plugin(MigrationTask[TITLE.name].value)
@dataclass
class ADBConnectionCheckerPlugin(ADBConnectionChecker):
    """Plugin for the ADBConnectionChecker task."""

    pass


# Signed off by Brian Sanford on 20260625
