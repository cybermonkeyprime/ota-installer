# src/ota_installer.tasks/components/t03_boot_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..operations.task_operation_processor import image_handler
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.EXTRACT_STOCK_BOOT_IMAGE.value


@task_plugin(PreparationTasks.EXTRACT_STOCK_BOOT_IMAGE.value)
@dataclass
class BootImageExtractor(BaseTask):
    """Extracts the stock boot image from a given payload file."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for extracting the boot image."""
        device = self.instance.file_name.device
        destination_path = Path.home() / "images"
        image_key = image_handler(device)
        options = self._format_options(image_key.stem, destination_path)
        command_string = self._build_command_string(options)

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    def _format_options(self, image_stem: str, destination: Path) -> str:
        """Formats the options for the payload dumper command."""
        return f'--partitions="{image_stem}" --out "{destination}"'

    def _build_command_string(self, options: str) -> str:
        """Constructs the command string for the payload dumper."""
        return f"payload_dumper {self.instance.file_paths.payload} {options}"

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to extract the boot image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260209
