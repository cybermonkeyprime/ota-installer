# src/ota_installer/dispatchers/factories/dispatch_retriever.py
from dataclasses import dataclass
from typing import Self

from ...log_setup import logger
from .mappings.dispatcher_factory_mapping import (
    DispatcherClasses,
    DispatcherType,
)


@dataclass
class DispatchRetriever(object):
    """
    Handles safe lookup and validation of dispatcher types from string keys.
    Backed by DispatcherType enum. Returns plugin dispatcher classes.
    """

    process_type: str

    def allowed_dispatchers(self) -> tuple[str, ...]:
        """Returns a tuple of allowed dispatcher names."""
        return tuple(enum_member.name for enum_member in DispatcherType)

    def set_function_call(self, function_call) -> Self:
        """Sets the function call for the dispatcher."""
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> DispatcherClasses | None:
        """Retrieves the dispatcher class based on the process type."""
        logger.debug(
            f"Retrieving dispatcher for process type: {self.process_type}"
        )
        if self.process_type.upper() not in self.allowed_dispatchers():
            logger.error(
                f"Invalid dispatcher type: {self.process_type}."
                f"Allowed: {self.allowed_dispatchers()}"
            )
            return None

        dispatcher_enum = DispatcherType[self.process_type.upper()]
        if dispatcher_enum is None:
            logger.error(f"Dispatcher mapping failed for: {self.process_type}")
            return None
        dispatcher_class = dispatcher_enum.value
        return dispatcher_class(self.function_call)


# Signed off by Brian Sanford on 20260213
