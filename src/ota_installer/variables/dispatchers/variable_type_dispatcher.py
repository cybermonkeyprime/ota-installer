# src/ota_installer/variables/dispatchers/variable_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

from ...dispatchers.constants.dispatcher_constants import DispatcherConstants
from ...dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ...dispatchers.templates.dispatcher_template import DispatcherTemplate


@dispatcher_plugin(DispatcherConstants.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        self.collection = {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths["log_file"],
        }
