# src/ota_installer/display/variable/processor/display_variable_handler.py
from dataclasses import dataclass
from enum import Enum
from typing import Self

from ..variable.variable_manager import VariableManager
from .variable.processor.directory_process_handler import (
    DirectoryIterationProcessor,
)
from .variable.processor.file_process_handler import (
    FileIterationProcessor,
    VariableFileProcessor,
)


@dataclass(frozen=True, slots=True)
class DisplayVariableRenderer:
    class_type: type
    mapping: dict[str, str | tuple]

    def __call__(self, variable_manager: VariableManager) -> None:
        instance = self.class_type(variable_manager)
        for key, value in self.mapping.items():
            instance.set_item(key, value)
        instance.process_items()


class DisplayVariableBehavior(Enum):
    """Base class for display variable behaviors."""

    def __call__(self, variable_manager: VariableManager) -> None:
        self.value(variable_manager)

    @classmethod
    def list(cls) -> tuple[DisplayVariableBehavior, ...]:
        """Returns a set of directory-related display variable definitions."""
        return tuple(cls)


class DisplayVariableDirectory(DisplayVariableBehavior):
    OTA = DisplayVariableRenderer(
        VariableFileProcessor,
        {"title": "ota_file_directory", "value": "path.parent"},
    )
    BOOT = DisplayVariableRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("stock", "magisk"),
            "directory_type": "",
            "variable_prefix": "",
        },
    )
    MAGISK = DisplayVariableRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("local", "remote"),
            "directory_type": "magisk",
            "variable_prefix": "_",
        },
    )


class DisplayVariableFile(DisplayVariableBehavior):
    OTA = DisplayVariableRenderer(
        VariableFileProcessor, {"title": "ota_file_name", "value": "path.name"}
    )
    IMAGE = DisplayVariableRenderer(
        FileIterationProcessor,
        mapping={"file_names": ("payload", "stock", "magisk")},
    )
    LOG = DisplayVariableRenderer(
        VariableFileProcessor, {"title": "log_file", "value": "log_file"}
    )


class DisplayVariableGroup(Enum):
    """Enumeration for grouping display variable definitions."""

    FILE = DisplayVariableFile.list()
    DIRECTORY = DisplayVariableDirectory.list()
    # LOG = (DisplayVariableFile.LOG,)

    def process(self, processor: VariableManager) -> None:
        """Executes a set of processing functions."""
        for enum_class in self.value:
            enum_class(processor)


@dataclass(frozen=True, slots=True)
class DisplayVariablePipeline:
    """Pipeline for processing display variables."""

    variable_manager: VariableManager

    def process_directory_names(self) -> Self:
        """Processes directory names."""
        DisplayVariableGroup.DIRECTORY.process(self.variable_manager)
        return self

    def process_file_names(self) -> Self:
        """Processes file names."""
        DisplayVariableGroup.FILE.process(self.variable_manager)
        return self


# Signed off by Brian Sanford on 20260608
