# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.EXTRACT_PAYLOAD_IMAGE.value


@task_plugin(PreparationTasks.EXTRACT_PAYLOAD_IMAGE.value)
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

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to extract the payload image."""
        self.task.run_with_output()


# Signed off by Brian Sanford on 20260129
