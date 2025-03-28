from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Optional

import build.dispatchers as dispatchers


@dataclass
class DispatcherManager(object):
    Class: Callable = field(default_factory=lambda: type)
    path: Path = field(default_factory=Path)
    allowed_objects: set = field(
        default_factory=lambda: {"directory", "file", "variable"}
    )

    def creator(self, object_type) -> Optional[dispatchers.MainDispatcher]:
        try:
            if object_type in self.allowed_objects:
                return dispatchers.MainDispatcher(object_type, self.Class(self.path))
        except Exception as err:
            print(err)
