# src/ota_installer/handler/variable_handler.py
from dataclasses import dataclass, field
from pathlib import Path

from ..dispatcher.dispatcher_handler import DispatcherTemplate
from ..dispatcher.dispatcher_info import DispatcherType
from ..plugin.plugin_registry import dispatcher_plugin

StrPathDict = dict[str, Path | str]


@dispatcher_plugin(name=DispatcherType.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling variable types."""

    obj: type = field(default_factory=lambda: type)
    collection: StrPathDict = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the collection of paths based on the provided object."""
        self.collection = self._initialize_collection()

    def _initialize_collection(self) -> StrPathDict:
        """Creates a collection of paths and log file."""
        return {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths.log_file,
        }


# Signed off by Brian Sanford on 20260523
