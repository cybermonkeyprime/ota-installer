# src/ota_installer/tasks/plugin_registry.py
from collections.abc import Callable

DISPATCHER_PLUGINS: dict[str, Callable] = {}


def dispatcher_plugin(name) -> Callable:
    """Decorator to register a dispatcher plugin."""

    def decorator(cls):
        DISPATCHER_PLUGINS[name] = cls
        return cls

    return decorator


# Signed off by Brian Sanford on 20260202
