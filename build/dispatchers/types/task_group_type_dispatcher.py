from dataclasses import dataclass, field
from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class TaskGroupTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "preparation": self.obj.preparation,
            "migration": self.obj.migration,
            "application": self.obj.application,
        }
