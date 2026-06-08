# src/ota_installer/display/variable/processor/variable_process_handler.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from ....variable.variable_manager import VariableManager
from .directory_process_handler import (
    DirectoryIterationProcessor,
)
from .file_process_handler import (
    FileIterationProcessor,
    VariableFileProcessor,
)


@dataclass(frozen=True, slots=True)
class ProcessorRenderer:
    class_type: type
    mapping: dict[str, str | tuple]

    def __call__(self, variable_manager: VariableManager) -> None:
        instance = self.class_type(variable_manager)
        for key, value in self.mapping.items():
            instance.set_item(key, value)
        instance.process_items()


class ProcessorConfig(Enum):
    OTA_DIRECTORY = ProcessorRenderer(
        VariableFileProcessor,
        {"title": "ota_file_directory", "value": "path.parent"},
    )
    BOOT_DIRECTORY = ProcessorRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("stock", "magisk"),
            "directory_type": "",
            "variable_prefix": "",
        },
    )
    MAGISK_DIRECTORY = ProcessorRenderer(
        DirectoryIterationProcessor,
        {
            "directory_names": ("local", "remote"),
            "directory_type": "magisk",
            "variable_prefix": "_",
        },
    )
    OTA_FILE = ProcessorRenderer(
        VariableFileProcessor, {"title": "ota_file_name", "value": "path.name"}
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
        return frozenset((cls.OTA_FILE, cls.IMAGE_FILE))


class ProcessorGroup(Enum):
    FILE = ProcessorConfig.files()
    DIRECTORY = ProcessorConfig.directories()
    LOG = ProcessorConfig.LOG_FILE

    def process_items(self) -> None:
        """Executes a set of processing functions."""
        if isinstance(self.value, frozenset):
            for enum_class in self.value:
                enum_class(self.processor)
            print()

    def process_item(self) -> None:
        """Processes the log file."""
        if not isinstance(self.value, frozenset):
            self.value(self.processor)
            print()

    @classmethod
    def process_file_names(cls) -> type:
        cls.FILE.process_items()
        return cls

    @classmethod
    def process_directory_names(cls) -> type:
        cls.DIRECTORY.process_items()
        return cls

    @classmethod
    def process_log_file(cls) -> type:
        cls.LOG.process_item()
        return cls

    @classmethod
    def set_processor(cls, processor: VariableManager):
        cls.processor = processor
        return cls


# Signed off by Brian Sanford on 20260608
