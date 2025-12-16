# src/ota_installer/dispatchers/dispatcher_interface.py
from dataclasses import dataclass, field

from ota_installer.dispatchers.factories.dispatcher_factory import (
    DispatcherTypes,
)

from .factories import DispatcherFactory


@dataclass
class DispatcherInterface(object):
    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def get_dispatcher(self) -> DispatcherTypes:
        dispatcher = DispatcherFactory()
        result = dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )
        return result

    def get_value(self, key: str):
        dispatcher = self.get_dispatcher()
        return dispatcher.get_value(key=key)
