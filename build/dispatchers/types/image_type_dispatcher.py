from dataclasses import dataclass, field
from typing import Any

from ..dispatcher_template import DispatcherTemplate


@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "shiba": "init_boot",
        }

    def get_key(self, key: str) -> Any:
        return self.collection.get(key, "boot")
