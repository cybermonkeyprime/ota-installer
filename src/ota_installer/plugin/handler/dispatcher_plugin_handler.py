# src/ota_installer/dispatchers/factories/plugin_dispatcher_adapter.py

from dataclasses import dataclass, field

from ...log_setup import logger
from ..plugin_registry import DISPATCHER_PLUGINS


@dataclass
class PluginDispatcherAdapter:
    """Adapter for loading and interacting with plugin dispatchers.

    This class provides a unified interface for loading dispatchers
    based on a type string and safely accessing their methods.
    """

    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def load(self) -> type | None:
        """Load the dispatcher based on the specified type."""
        logger.debug(f"Loading dispatcher: {self.dispatcher}")
        return load_plugin_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )

    def get_value(self, key: str) -> object:
        """Retrieve a value from the dispatcher using the specified key."""
        dispatcher = self.load()
        if not dispatcher:
            logger.error(
                f"Failed to load dispatcher '{self.dispatcher}'. "
                f"Cannot retrieve value for key: {key}"
            )
            return None
        return dispatcher.get_value(key=key)


def load_plugin_dispatcher(dispatcher_type: str, obj: type) -> type | None:
    """Load a registered plugin dispatcher based on the dispatcher type."""
    logger.debug(f"Loading plugin dispatcher for type: {dispatcher_type}")
    dispatcher_class = DISPATCHER_PLUGINS.get(dispatcher_type)

    if not dispatcher_class:
        logger.error(
            f"No plugin dispatcher registered for: {dispatcher_type!r}",
        )
        return None

    return dispatcher_class(obj)
