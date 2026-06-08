# src/ota_installer/display/variables/functions.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from ...variable.variable_manager import VariableManager
from ..variable.processor.directory_process_handler import (
    DirectoryIterationProcessor,
)
from ..variable.processor.file_process_handler import (
    FileIterationProcessor,
    VariableFileProcessor,
)


@dataclass(frozen=True, slots=True)
class ProcessorRenderer:
    Class: type
    mapping: dict[str, str | tuple]

    def __call__(self, variable_manager: VariableManager) -> None:
        _object = self.Class(variable_manager)
        for key, value in self.mapping.items():
            _object.set_item(key, value)
        _object.process_items()


class ProcessorConfig(Enum):
    OTA_DIRECTORY = ProcessorRenderer(
        VariableFileProcessor,
        {"title": "ota_file_directory", "value": "path.parent"},
    )
    MAGISK_DIRECTORY = ProcessorRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("local", "remote"),
            "directory_type": "magisk",
            "variable_prefix": "_",
        },
    )
    BOOT_DIRECTORY = ProcessorRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("stock", "magisk"),
            "directory_type": "",
            "variable_prefix": "",
        },
    )
    OTA_NAME = ProcessorRenderer(
        VariableFileProcessor,
        {"title": "ota_file_name", "value": "path.name"},
    )
    IMAGE_FILE = ProcessorRenderer(
        FileIterationProcessor,
        mapping={"file_names": ("payload", "stock", "magisk")},
    )
    LOG_FILE = ProcessorRenderer(
        VariableFileProcessor, {"title": "log_file", "value": "log_file"}
    )

    def __call__(self, variable_manager: VariableManager) -> None:
        self.value(variable_manager)

    @classmethod
    def directories(cls) -> frozenset[Callable]:
        return frozenset(
            (cls.OTA_DIRECTORY, cls.BOOT_DIRECTORY, cls.MAGISK_DIRECTORY)
        )

    @classmethod
    def files(cls) -> frozenset[Callable]:
        return frozenset((cls.OTA_NAME, cls.IMAGE_FILE))

    @classmethod
    def process_items(
        cls, enum_classes: frozenset[Callable], processor: VariableManager
    ) -> None:
        """Executes a set of processing functions."""
        for enum_class in enum_classes:
            enum_class(processor)
