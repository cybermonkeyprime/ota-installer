# src/ota_installer/variable/variable_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

from ..dispatcher.dispatcher_template import DispatcherTemplate
from ..dispatcher.dispatcher_type import DispatcherType
from ..plugin.plugin_registry import Plugin


@Plugin.DISPATCHER.register(name=DispatcherType.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling variable types."""

    obj: type = field(default_factory=lambda: type)
    collection: dict[str, str | Path] = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the collection of paths based on the provided object."""
        self.collection = self._initialize_collection()

    def _initialize_collection(self) -> dict[str, str | Path]:
        """Creates a collection of paths and log file."""
        return {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths.log_file,
        }


# Signed off by Brian Sanford on 20260902
