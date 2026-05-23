# src/ota_installer.tasks/components/04_stock_boot_image_backuppper.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task_group.task_group_handler import PreparationTask
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from ..operation.task_operation_processor import image_handler
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BACKUP_STOCK_BOOT_IMAGE.value


@task_plugin(PreparationTask.BACKUP_STOCK_BOOT_IMAGE.value)
@dataclass
class StockBootImageBackupper(BaseTask):
    """Task to backup the stock boot image to a specified path."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """
        Initialize the command string for backing up the stock boot image.
        """
        image_path = Path(image_handler(self.instance.file_name.device))
        command_string = f"cp -v {image_path} {self.instance.file_paths.stock}"

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorator.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished successfully!"
    )
    def perform_task(self) -> None:
        """Execute the task to backup the stock boot image."""
        self.task.run_with_output()
