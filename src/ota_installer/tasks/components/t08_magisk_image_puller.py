# src/ota_installer/tasks/components/t08_magisk_image_puller.py
from dataclasses import dataclass, field

from loguru import logger

from ... import decorators
from ...images.magisk_image.constants.magisk_image_paths import (
    MagiskImagePaths,
)
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...task_groups.constants.migration_tasks import MigrationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PULL_MAGISK_IMAGE.value


@task_plugin(MigrationTasks.PULL_PATCHED_BOOT_IMAGE.value)
@dataclass
class MagiskImagePuller(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        source = (
            MagiskImagePaths.REMOTE_PATH.value
            / self.instance.image_name["patched"]
        )
        destination = (
            MagiskImagePaths.LOCAL_PATH.value
            / self.instance.file_paths["magisk"]
        )

        command_string = f'adb pull "{source}" "{destination}"'

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
        logger.debug(f"{ApplicationTasks.REBOOT_TO_BOOTLOADER.value=}")
