# src/ota_installer/tasks/components/t08_magisk_image_puller.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...image.magisk_image_handler import (
    MagiskImagePath,
)
from ...log_setup import logger
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import ApplicationTask, MigrationTask
from ...variable.variable_manager import VariableManager
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.PULL_MAGISK_IMAGE


@dataclass
class MagiskImagePuller(BaseTask):
    """Task to pull the patched boot image using adb."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for pulling the image."""
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=self._build_command(),
        )

    def _build_command(self) -> str:
        """Constructs the adb pull command string."""
        return (
            f'adb pull "{self._get_source_path()}" '
            f'"{self._get_destination_path()}"'
        )

    def _get_source_path(self) -> Path:
        """Constructs the source path for the patched boot image."""
        return (
            MagiskImagePath.REMOTE_PATH.value
            / self.instance.image_name["patched"]
        )

    def _get_destination_path(self) -> Path:
        """Constructs the destination path for the pulled image."""
        return (
            MagiskImagePath.LOCAL_PATH.value / self.instance.file_paths.magisk
        )

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to pull the patched boot image."""
        self.task.run_with_output()
        logger.debug(f"{ApplicationTask.REBOOT_TO_BOOTLOADER.value=}")


@task_plugin(MigrationTask[TITLE.name].value)
@dataclass
class MagiskImagePullerPlugin(MagiskImagePuller):
    """Plugin for the MagiskImagePuller task."""

    pass


# Signed off by Brian Sanford on 20260528
