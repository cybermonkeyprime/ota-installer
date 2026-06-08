from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from ....variable.variable_manager import VariableManager
from ...variable.variable_functions import ProcessorConfig


@dataclass(slots=True)
class VariableProcessor:
    """Processes variable file and directory names for OTA installation."""

    variable_manager: VariableManager

    def process_file_names(self) -> Self:
        """Processes OTA and image file names."""
        self._process_items(ProcessorConfig.files())
        return self

    def process_directory_names(self) -> Self:
        """Processes OTA, boot image, and Magisk image directory names."""
        self._process_items(ProcessorConfig.directories())
        print()
        return self

    def _process_items(self, enum_classes: frozenset[Callable]) -> None:
        """Executes a set of processing functions."""
        for enum_class in enum_classes:
            enum_class(self.variable_manager)

    def process_log_file(self) -> Self:
        """Processes the log file."""
        ProcessorConfig.LOG_FILE(self.variable_manager)
        print()
        return self
