# src/ota_installer/tasks/components/t08_magisk_image_puller.py
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from ... import decorators
from ...images.magisk_image.constants.magisk_image_paths import (
    MagiskImagePaths,
)
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...task_groups.constants.migration_task import MigrationTask
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PULL_MAGISK_IMAGE.value


@task_plugin(MigrationTask.PULL_PATCHED_BOOT_IMAGE.value)
@dataclass
class MagiskImagePuller(BaseTask):
    """Task to pull the patched boot image using adb."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for pulling the image."""
        command_string = self._build_command_string()

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    def _build_command_string(self) -> str:
        """Constructs the adb pull command string."""
        return f'adb pull "{self._get_source_path()}" "{self._get_destination_path()}"'

    def _get_source_path(self) -> Path:
        """Constructs the source path for the patched boot image."""
        return (
            MagiskImagePaths.REMOTE_PATH.value
            / self.instance.image_name["patched"]
        )

    def _get_destination_path(self) -> Path:
        """Constructs the destination path for the pulled image."""
        return (
            MagiskImagePaths.LOCAL_PATH.value / self.instance.file_paths.magisk
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to pull the patched boot image."""
        self.task.run_with_output()
        logger.debug(f"{ApplicationTasks.REBOOT_TO_BOOTLOADER.value=}")


