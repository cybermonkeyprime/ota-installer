# src/ota_installer.tasks/components/t03_boot_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import PreparationTask
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_processor import image_handler
from ..task_info import TaskID
from .base_task import BaseTask

TITLE = TaskID.EXTRACT_STOCK_BOOT_IMAGE


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
            enum_values=TITLE.enum_values,
            command_string=command_string,
        )

    def _format_options(self, image_stem: str, destination: Path) -> str:
        """Formats the options for the payload dumper command."""
        return f'--partitions="{image_stem}" --out "{destination}"'

    def _build_command_string(self, options: str) -> str:
        """Constructs the command string for the payload dumper."""
        return f"payload_dumper {self.instance.file_paths.payload} {options}"

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to extract the boot image."""
        self.task.run_with_output()


@task_plugin(PreparationTask[TITLE.name].value)
@dataclass
class BootImageExtractorPlugin(BootImageExtractor):
    """Plugin for the BootImageExtractor task."""

    pass


