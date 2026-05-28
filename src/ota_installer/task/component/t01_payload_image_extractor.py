# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...handler.task_group_handler import PreparationTask
from ...plugin.plugin_registry import task_plugin
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from .base_task import BaseTask

TITLE = "EXTRACT_PAYLOAD_IMAGE"
ENUM_VALUES = TaskOperationDetails[TITLE].value


@task_plugin(name=PreparationTask[TITLE].value)
@dataclass
class PayloadImageExtractor(BaseTask):
    """Extracts payload images from a specified archive file."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self):
        """Initializes the command string for extracting the payload image."""
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=self._create_extraction_command(),
        )

    def _create_extraction_command(self) -> str:
        """Constructs the command string for extraction."""
        return f'7z e "{self.instance.path}" payload.bin -o"{Path.home()}" -y'

    @decorator.DoublePaddedFooterWrapper(
        message=f"{TaskOperationDetails[TITLE].success_message}"
    )
    def perform_task(self) -> None:
        """Executes the task to extract the payload image."""
        self.task.run_with_output()
