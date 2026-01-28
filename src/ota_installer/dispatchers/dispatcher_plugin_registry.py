# src/ota_installer/tasks/plugin_registry.py
from collections.abc import Callable

DISPATCHER_PLUGINS = {}


def dispatcher_plugin(name) -> Callable:
    """Decorator to register a dispatcher plugin."""

    def decorator(cls):
        DISPATCHER_PLUGINS[name] = cls
        return cls

    return decorator


