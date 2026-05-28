# src/ota_installer/tasks/components/t05_adb_connection_checker.py
from dataclasses import dataclass, field

from ... import decorator
from ...handler.task_group_handler import MigrationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "CHECK_ADB_CONNECTION"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


@task_plugin(MigrationTask[TITLE].value)
@dataclass
class ADBConnectionChecker(BaseTask):
    """Checks the ADB connection status and performs the task."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the ADBConnectionChecker with command string."""
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=ENUM_VALUES.command_string,
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Executes the ADB connection check task."""
        self.task.run_with_output()
