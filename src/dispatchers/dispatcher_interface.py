from dataclasses import dataclass, field

from .factories import DispatcherFactory
from .templates import DispatcherTemplate


@dataclass
class DispatcherInterface(object):
    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def get_dispatcher(self) -> DispatcherTemplate:
        dispatcher = DispatcherFactory()
        return dispatcher.create_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )

    def get_value(self, key: str):
        dispatcher = self.get_dispatcher()
        return dispatcher.get_value(key=key)
