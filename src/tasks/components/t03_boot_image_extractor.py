# src/tasks/components/t03_boot_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

import src.tasks as tasks
import src.variables as variables
from src import decorators
from src.tasks.task_operation_processor import (
    image_handler,
)

from .base_task import BaseTask

ENUM_VALUES = tasks.TaskOperationDetails.BOOT_IMAGE_EXTRACTOR.value


@dataclass
class BootImageExtractor(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        device = self.instance.file_name_parser.device
        source_path = self.instance.boot_image_paths.payload
        destination_path = Path.home() / "images"
        image_key = image_handler(device)
        options = f'--images="{image_key}" --out "{destination_path}"'
        command_string = f"payload_dumper {source_path} {options}"

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
