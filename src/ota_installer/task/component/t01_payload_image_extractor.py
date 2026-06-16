# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import PreparationTask
from ...task.task_info import TaskID
from ...variable.variable_manager import VariableManager
from .base_task import BaseTask

TITLE = TaskID.EXTRACT_PAYLOAD_IMAGE


@dataclass
class PayloadImageExtractor(BaseTask):
    """Extracts payload images from a specified archive file."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self):
        """Initializes the command string for extracting the payload image."""
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=self._create_extraction_command(),
        )

    def _create_extraction_command(self) -> str:
        """Constructs the command string for extraction."""
        return f'7z e "{self.instance.path}" payload.bin -o"{Path.home()}" -y'

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to extract the payload image."""
        self.task.run_with_output()


@task_plugin(PreparationTask[TITLE.name].value)
@dataclass
class PayloadImageExtractorPlugin(PayloadImageExtractor):
    """Plugin for the PayloadImageRenamer task."""

    pass


# Signed off by Brian Sanford on 20260528
