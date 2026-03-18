# src/ota_installer/tasks/components/t05_adb_connection_checker.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.migration_task import MigrationTask
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.CHECK_ADB_CONNECTION.value


@task_plugin(MigrationTask.CHECK_ADB_CONNECTION.value)
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

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished successfully!"
    )
    def perform_task(self) -> None:
        """Executes the ADB connection check task."""
        self.task.run_with_output()


