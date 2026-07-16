# src/ota_installer.tasks/components/04_stock_boot_image_backuppper.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import Plugin
from ...task.task_group_info import PreparationTask
from ...variable.variable_director import VariableDirector
from ..operation.task_operation_processor import image_handler
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.BACKUP_STOCK_BOOT_IMAGE


@dataclass
class StockBootImageBackupper(BaseTask):
    """Task to backup the stock boot image to a specified path."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """
        Initialize the command string for backing up the stock boot image.
        """
        self.command_string = self._create_command_string()
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=self._create_command_string(),
        )

    def _create_command_string(self) -> str:
        """Create the command string for the backup operation."""
        image_path = Path(image_handler(self.instance.file_name.device))
        return f"cp -v {image_path} {self.instance.file_paths.stock}"

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Execute the task to backup the stock boot image."""
        self.task.run_with_output()


@Plugin.TASK.register(PreparationTask[TITLE.name].value)
@dataclass
class StockBootImageBackupperPlugin(StockBootImageBackupper):
    """Plugin for the StockBootImageBackupper task."""

    pass


# Signed off by Brian Sanford on 20260625
