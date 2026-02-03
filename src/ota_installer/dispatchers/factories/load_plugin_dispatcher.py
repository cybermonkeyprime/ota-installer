# src/ota_installer/dispatchers/factories/load_plugin_dispatcher.py
from ...log_setup import logger
from ..dispatcher_plugin_registry import DISPATCHER_PLUGINS


def load_plugin_dispatcher(dispatcher_type: str, obj: type) -> type | None:
    """Load a registered plugin dispatcher based on the dispatcher type."""

    logger.debug(f"load_plugin_dispatcher(): {dispatcher_type=}")
    dispatcher_class = DISPATCHER_PLUGINS.get(dispatcher_type)
    logger.debug(f"load_plugin_dispatcher(): {dispatcher_class=}")
    if not dispatcher_class:
        logger.error(
            f"No plugin dispatcher registered for: {dispatcher_type!r}",
        )
        return None
    return dispatcher_class(obj)


# Signed off by Brian Sanford on 20260203
