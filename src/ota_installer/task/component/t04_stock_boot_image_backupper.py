# src/ota_installer.tasks/components/04_stock_boot_image_backuppper.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...handler.task_group_handler import PreparationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from ..operation.task_operation_processor import image_handler
from .base_task import BaseTask

TITLE = "BACKUP_STOCK_BOOT_IMAGE"
TASK_OPS = TaskOperationDetails[TITLE]
ENUM_VALUES = TASK_OPS.value


@task_plugin(PreparationTask[TITLE].value)
@dataclass
class StockBootImageBackupper(BaseTask):
    """Task to backup the stock boot image to a specified path."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """
        Initialize the command string for backing up the stock boot image.
        """
        self.command_string = self._create_command_string()
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=self._create_command_string(),
        )

    def _create_command_string(self) -> str:
        """Create the command string for the backup operation."""
        image_path = Path(image_handler(self.instance.file_name.device))
        return f"cp -v {image_path} {self.instance.file_paths.stock}"

    @decorator.DoublePaddedFooterWrapper(message=f"{TASK_OPS.success_message}")
    def perform_task(self) -> None:
        """Execute the task to backup the stock boot image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260527
