# src/ota_installer/tasks/components/t06_stock_boot_image_pusher.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.migration_task import MigrationTask
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PUSH_STOCK_BOOT_IMAGE.value


@task_plugin(MigrationTask.PUSH_STOCK_BOOT_IMAGE.value)
@dataclass
class StockBootImagePusher(BaseTask):
    """Task to push the stock boot image to the device using adb."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for pushing the stock boot image."""
        command_string = self._create_command_string()

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
            reminder=ENUM_VALUES.REMINDER.value,
        )

    def _create_command_string(self) -> str:
        """Creates the adb push command string."""
        stock_image_path = Path(self.instance.file_paths.stock)
        return f'adb push "{stock_image_path}" /sdcard/'

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to push the stock boot image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260116
