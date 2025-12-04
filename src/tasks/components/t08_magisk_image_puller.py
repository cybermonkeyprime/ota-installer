# src/tasks/components/t08_magisk_image_puller.py
from dataclasses import dataclass, field
from pathlib import Path

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PULL_MAGISK_IMAGE.value


@dataclass
class MagiskImagePuller(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        magisk_path = self.instance.boot_image_paths.magisk
        magisk_directory = self.instance.directory.magisk_image

        magisk_local_path = Path(magisk_directory.local_path)
        magisk_remote_path = Path(magisk_directory.remote_path)

        source_path: Path = (
            Path(magisk_remote_path) / self.instance.patched_image_name
        )
        destination_path = (
            Path.home() / magisk_local_path / magisk_path.file_name
        )

        command_string = f'adb pull "{source_path}" "{destination_path}"'

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
