# src/ota_installer/dispatchers/factories/plugin_dispatcher_adapter.py

"""
plugin_dispatcher_adapter.py

Adapter that wraps dispatcher instantiation via the plugin system.
Acts as a unified interface for downstream tasks to:
- Load dispatcher based on type string
- Safely access dispatcher methods (e.g., `.get_value()`)

Useful in display processors and variable extraction workflows.
"""

from dataclasses import dataclass, field

from ...log_setup import logger
from ..factories.load_plugin_dispatcher import (
    load_plugin_dispatcher,
)


@dataclass
class PluginDispatcherAdapter(object):
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


# Signed off by Brian Sanford on 20260203
