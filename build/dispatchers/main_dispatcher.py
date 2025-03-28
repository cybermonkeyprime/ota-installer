from dataclasses import dataclass, field
from typing import Any, Optional, Union
from pathlib import Path

from build.dispatchers import DispatcherTemplate, DispatcherFactory


@dataclass
class MainDispatcher(object):
    dispatcher: str = field(default_factory=str)
    object_processer: Any = field(default_factory=lambda: "")

    @property
    def _dispatcher(self) -> DispatcherTemplate:
        dispatcher = DispatcherFactory()
        return dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processer
        )

    def receiver(self) -> DispatcherTemplate:
        return self._dispatcher

    def get_value(self, key: str = "") -> Optional[Union[type, Path, None]]:
        return self._dispatcher.get_value(key=key)
