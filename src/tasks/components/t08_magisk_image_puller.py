# src/tasks/components/t08_magisk_image_puller.py
from dataclasses import dataclass, field

import src.variables as variables
from src import decorators
from src.paths.constants import MagiskImagePaths
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PULL_MAGISK_IMAGE.value


@dataclass
class MagiskImagePuller(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

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
