from dataclasses import dataclass, field
from typing import Any

from build.dispatchers import DispatcherTemplate, DispatcherFactory


@dataclass
class MainDispatcher:
    dispatcher: str = field(default_factory=str)
    object_processer: Any = field(default_factory=lambda: "")

    def get_dispatcher(self) -> DispatcherTemplate:
        dispatcher = DispatcherFactory()
        return dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processer
        )

    def get_value(self, key: str):
        return self.get_dispatcher().get_value(key=key)
