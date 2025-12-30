# src/ota_installer/dispatchers/dispatcher_interface.py
from dataclasses import dataclass, field

from ...log_setup import logger
from ..constants.dispatcher_mapping import DispatcherTypes
from ..factories.dispatch_factory import create_dispatcher


@dataclass
class DispatcherInterface(object):
    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def get_dispatcher(self) -> DispatcherTypes | None:
        logger.debug(f"{self.dispatcher=}")
        return create_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )

    def get_value(self, key: str):
        dispatcher = self.get_dispatcher()
        return dispatcher.get_value(key=key)  # pyright: ignore[reportOptionalMemberAccess,reportAttributeAccessIssue]
