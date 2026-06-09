# src/ota_installer/display/variable/processor/display_variable_handler.py
from collections.abc import Callable
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


class DisplayVariableDefinition(Enum):
    OTA_DIRECTORY = DisplayVariableRenderer(
        VariableFileProcessor,
        {"title": "ota_file_directory", "value": "path.parent"},
    )
    BOOT_DIRECTORY = DisplayVariableRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("stock", "magisk"),
            "directory_type": "",
            "variable_prefix": "",
        },
    )
    MAGISK_DIRECTORY = DisplayVariableRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("local", "remote"),
            "directory_type": "magisk",
            "variable_prefix": "_",
        },
    )
    OTA_FILE = DisplayVariableRenderer(
        VariableFileProcessor, {"title": "ota_file_name", "value": "path.name"}
    )
    IMAGE_FILE = DisplayVariableRenderer(
        FileIterationProcessor,
        mapping={"file_names": ("payload", "stock", "magisk")},
    )
    LOG_FILE = DisplayVariableRenderer(
        VariableFileProcessor, {"title": "log_file", "value": "log_file"}
    )

    def __call__(self, variable_manager: VariableManager) -> None:
        self.value(variable_manager)

    @classmethod
    def directories(cls) -> frozenset[Callable]:
        """Returns a set of directory-related display variable definitions."""
        return frozenset(
            (cls.OTA_DIRECTORY, cls.BOOT_DIRECTORY, cls.MAGISK_DIRECTORY)
        )

    @classmethod
    def files(cls) -> frozenset[Callable]:
        """Returns a set of file-related display variable definitions."""
        return frozenset((cls.OTA_FILE, cls.IMAGE_FILE))


class DisplayVariableGroup(Enum):
    """Enumeration for grouping display variable definitions."""

    FILE = DisplayVariableDefinition.files()
    DIRECTORY = DisplayVariableDefinition.directories()
    LOG = (DisplayVariableDefinition.LOG_FILE,)

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

    def process_log_file(self) -> Self:
        """Processes the log file."""
        DisplayVariableGroup.LOG.process(self.variable_manager)
        return self


# Signed off by Brian Sanford on 20260608
