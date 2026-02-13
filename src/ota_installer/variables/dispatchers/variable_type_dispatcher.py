# src/ota_installer/variables/dispatchers/variable_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ...dispatchers.templates.dispatcher_template import DispatcherTemplate


@dispatcher_plugin(DispatcherConstants.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling variable types."""

    obj: type = field(default_factory=lambda: type)
    collection: dict[str, Path | str] = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the collection of paths based on the provided object."""
        self.collection = self._initialize_collection()

    def _initialize_collection(self) -> dict[str, Path | str]:
        """Creates a collection of paths and log file."""
        return {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths.log_file,
        }


# Signed off by Brian Sanford on 20260213
