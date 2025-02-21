from dataclasses import dataclass, field
from typing import Any
from pathlib import Path
from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.log_file,
        }
