# src/ota_installer.tasks/components/t03_boot_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...tasks import TaskOperationDetails
from ...variables import VariableManager
from ..mappings.constants import TaskName
from ..plugin_registry import task_plugin
from ..task_operation_processor import (
    image_handler,
)
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BOOT_IMAGE_EXTRACTOR.value


@task_plugin(TaskName.EXTRACT_STOCK_BOOT_IMAGE.lower_case)
@dataclass
class BootImageExtractor(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        device = self.instance.file_name["device"]
        destination_path = Path.home() / "images"
        image_key = image_handler(device)
        options = f'--images="{image_key}" --out "{destination_path}"'
        command_string = (
            f"payload_dumper {self.instance.file_paths['payload']} {options}"
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
