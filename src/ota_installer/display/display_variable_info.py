# src/ota_installer/display/variable/processor/display_variable_info.py
from dataclasses import dataclass
from typing import Self

from ..variable.variable_manager import VariableManager
from .variable.processor.directory_process_info import (
    DirectoryIterationProcessor,
)
from .variable.processor.file_process_info import (
    FileIterationProcessor,
    VariableFileProcessor,
)


@dataclass(frozen=True, slots=True)
class DisplayStep:
    name: str
    processor_type: type
    config: dict[str, object]

    def build(self, variable_manager: VariableManager):
        processor = self.processor_type(variable_manager)

        for key, value in self.config.items():
            processor.set_item(key, value)

        return processor

    def run(self, variable_manager: VariableManager) -> None:
        processor = self.build(variable_manager)
        processor.process_items()


DIRECTORY_DISPLAY_STEPS = (
    DisplayStep(
        name="ota_file_directory",
        processor_type=VariableFileProcessor,
        config={
            "title": "ota_file_directory",
            "value": "path.parent",
        },
    ),
    DisplayStep(
        name="boot_directories",
        processor_type=DirectoryIterationProcessor,
        config={
            "source": "directory.boot_image",
            "directory_names": ("stock", "magisk"),
            "directory_type": "",
            "variable_prefix": "",
        },
    ),
    DisplayStep(
        name="magisk_directories",
        processor_type=DirectoryIterationProcessor,
        config={
            "source": "directories.magisk",
            "directory_names": ("local", "remote"),
            "directory_type": "magisk",
            "variable_prefix": "_",
        },
    ),
)


FILE_DISPLAY_STEPS = (
    DisplayStep(
        name="ota_file_name",
        processor_type=VariableFileProcessor,
        config={
            "title": "ota_file_name",
            "value": "path.name",
        },
    ),
    DisplayStep(
        name="image_file_names",
        processor_type=FileIterationProcessor,
        config={
            "file_names": ("payload", "stock", "magisk"),
        },
    ),
    DisplayStep(
        name="log_file",
        processor_type=VariableFileProcessor,
        config={
            "title": "log_file",
            "value": "log_file",
        },
    ),
)


def process_display_steps(
    variable_manager: VariableManager,
    steps: tuple[DisplayStep, ...],
) -> None:
    for step in steps:
        step.run(variable_manager)


def process_directory_display(variable_manager: VariableManager) -> None:
    process_display_steps(variable_manager, DIRECTORY_DISPLAY_STEPS)


def process_file_display(variable_manager: VariableManager) -> None:
    process_display_steps(variable_manager, FILE_DISPLAY_STEPS)


@dataclass(frozen=True, slots=True)
class DisplayVariablePipeline:
    variable_manager: VariableManager

    def process_directory_names(self) -> Self:
        process_directory_display(self.variable_manager)
        return self

    def process_file_names(self) -> Self:
        process_file_display(self.variable_manager)
        return self
