# src/ota_installer.tasks/components/04_stock_boot_image_backuppper.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..operations.task_operation_processor import image_handler
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BACKUP_STOCK_BOOT_IMAGE.value


@task_plugin(PreparationTasks.BACKUP_STOCK_BOOT_IMAGE.value)
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

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished successfully!"
    )
    def perform_task(self) -> None:
        """Execute the task to backup the stock boot image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260129
