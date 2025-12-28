# src/ota_installer.tasks/components/t03_boot_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..operations.task_operation_processor import image_handler
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.EXTRACT_STOCK_BOOT_IMAGE.value


@task_plugin(PreparationTasks.EXTRACT_STOCK_BOOT_IMAGE.value)
@dataclass
class BootImageExtractor(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        device = self.instance.file_name["device"]
        destination_path = Path.home() / "images"
        image_key = image_handler(device)
        options = f'--images="{image_key.stem}" --out "{destination_path}"'
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
