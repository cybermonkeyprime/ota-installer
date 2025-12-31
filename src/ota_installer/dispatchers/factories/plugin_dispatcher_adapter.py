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
from .mappings.dispatcher_factory_mapping import DispatcherTypes


@dataclass
class PluginDispatcherAdapter(object):
    """
    Adapter class that wraps dispatcher creation and provides
    a simplified interface for interacting with dispatcher logic.
    """

    dispatcher: str = field(default_factory=str)
    object_processor: type = field(default=type)

    def load(self) -> DispatcherTypes | None:
        logger.debug(f"PluginDispatcherAdapter.load(): {self.dispatcher=}")
        return load_plugin_dispatcher(
            dispatcher_type=self.dispatcher, obj=self.object_processor
        )

    def get_value(self, key: str):
        dispatcher = self.load()
        if not dispatcher:
            logger.error(
                f"Dispatcher '{self.dispatcher}' failed to load."
                f"Cannot retrieve value for key: {key}"
            )
            return None
        return dispatcher.get_value(key=key)  # pyright: ignore[reportOptionalMemberAccess,reportAttributeAccessIssue]
