# src/dispatchers/types/variable_type_dispatcher.py
from dataclasses import dataclass, field
from pathlib import Path

from ..templates import DispatcherTemplate


@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        self.collection = {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.log_file,
        }
