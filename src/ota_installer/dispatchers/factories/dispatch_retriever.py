# src/ota_installer/dispatchers/factories/dispatch_retriever.py
from dataclasses import dataclass
from typing import Self

from ...log_setup import logger
from .mappings.dispatcher_factory_mapping import (
    DispatcherFactoryMapping,
    DispatcherTypes,
)


@dataclass
class DispatchRetriever(object):
    """
    Handles safe lookup and validation of dispatcher types from string keys.
    Backed by DispatcherFactoryMapping enum. Returns plugin dispatcher classes.
    """

    process_type: str

    def allowed_dispatchers(self) -> tuple[str, ...]:
        return tuple(
            enum_member.name for enum_member in DispatcherFactoryMapping
        )

    def set_function_call(self, function_call) -> Self:
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> DispatcherTypes | None:
        logger.debug(
            f"DispatchRetriever.get_dispatcher(): {self.process_type=}"
        )
        allowed = self.allowed_dispatchers()
        if self.process_type.upper() not in self.allowed_dispatchers():
            logger.error(
                f"Invalid dispatcher type: {self.process_type}."
                f"Allowed: {allowed}"
            )
            return None

        try:
            dispatcher_enum = DispatcherFactoryMapping[
                self.process_type.upper()
            ]
            dispatcher_class = dispatcher_enum.value
            return dispatcher_class(self.function_call)
        except KeyError as e:
            logger.error(f"Dispatcher mapping failed: {e}")
            return None
