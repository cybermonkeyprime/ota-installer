# src/ota_installer/dispatchers/dispatcher_interface.py
from dataclasses import dataclass, field

from .factories.dispatch_factory import DispatcherTypes, dispatch_creator


@dataclass
class DispatcherInterface(object):
    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def get_dispatcher(self) -> DispatcherTypes:
        return dispatch_creator(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )

    def get_value(self, key: str):
        dispatcher = self.get_dispatcher()
        return dispatcher.get_value(key=key)  # pyright: ignore[reportAttributeAccessIssue]
