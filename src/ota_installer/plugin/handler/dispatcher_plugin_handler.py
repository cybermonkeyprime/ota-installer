# src/ota_installer/plugin/handler/dispatcher_plugin_handler.py
from dataclasses import dataclass, field

from ...dispatcher.dispatcher_info import DispatcherType
from ...log_setup import logger
from ..plugin_registry import Plugin


class DispatcherError(Exception):
    """Custom exception for dispatcher errors."""

    pass


@dataclass
class PluginDispatcherAdapter:
    """Adapter for loading and interacting with plugin dispatchers.

    This class provides a unified interface for loading dispatchers
    based on a type string and safely accessing their methods.
    """

    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def load(self) -> object:
        """Load the dispatcher based on the specified type."""
        logger.debug(f"Loading dispatcher: {self.dispatcher}")
        if self.dispatcher not in DispatcherType:
            message = f"{self.dispatcher.upper()} not found in DispatcherType"
            logger.error(message)
            raise DispatcherError(message)
        return self._load_plugin_dispatcher(
            dispatcher_type=self.dispatcher,
            obj=self.object_processor,
        )

    def _load_plugin_dispatcher(
        self, dispatcher_type: str, obj: type
    ) -> object:
        """Load a registered plugin dispatcher based on the dispatcher type."""
        logger.debug(f"Loading plugin dispatcher for type: {dispatcher_type}")
        valid_dispatcher = DispatcherType(dispatcher_type)
        dispatcher_class = Plugin.DISPATCHER[valid_dispatcher]

        if dispatcher_class is None:
            message = (
                f"No plugin dispatcher registered for: {valid_dispatcher!r}",
            )
            logger.error(message)
            raise DispatcherError(message)

        return dispatcher_class(obj)


# Signed off by Brian Sanford on 20260625
