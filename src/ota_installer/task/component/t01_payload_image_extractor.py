# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task_group.task_group_pipeline import PREPARATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = PREPARATION[0]
TITLE = STEP.name


@dataclass
class PayloadImageExtractor(BaseTask):
    """Extracts payload images from a specified archive file."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self):
        """Initializes the command string for extracting the payload image."""
        super().__init__(
            enum_values=STEP,
            command_string=self._create_extraction_command(),
        )

    def _create_extraction_command(self) -> str:
        """Constructs the command string for extraction."""
        return f'7z e "{self.instance.path}" payload.bin -o"{Path.home()}" -y'

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the task to extract the payload image."""
        self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class PayloadImageExtractorPlugin(PayloadImageExtractor):
    """Plugin for the PayloadImageRenamer task."""

    pass


# Signed off by Brian Sanford on 20260903
