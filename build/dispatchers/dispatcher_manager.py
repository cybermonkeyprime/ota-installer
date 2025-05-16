from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional, Union

from build.dispatchers import DispatcherMapper, DispatcherTemplate


@dataclass
class DispatcherManager(object):
    """
    Manages the creation and interaction with different types of dispatchers.

    Attributes:
        dispatcher_type: The type of dispatcher to be created.
        processor: The processor object to be used by the dispatcher.
    """

    dispatcher_type: str = field(default_factory=str)
    object_processer: Any = field(default_factory=lambda: "")

    def create_dispatcher(self) -> DispatcherTemplate:
        dispatcher = DispatcherMapper()
        return dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher_type, obj=self.object_processer
        )

    def get_dispatcher(self) -> DispatcherTemplate:
        return self.create_dispatcher()

    def get_value(self, key: str = "") -> Optional[Union[type, Path, None]]:
        return self.get_dispatcher().get_value(key=key)
