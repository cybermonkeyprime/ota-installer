from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    @property
    def collection(self) -> dict[str, Any]:
        return {
            "path.name": Path(self.obj.file_path).name,
            "path.parent": Path(self.obj.file_path).parent,
            "log_file": self.obj.log_file,
        }
