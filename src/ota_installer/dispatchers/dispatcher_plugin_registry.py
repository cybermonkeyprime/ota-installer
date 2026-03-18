# src/ota_installer/tasks/plugin_registry.py
from collections.abc import Callable

DISPATCHER_PLUGINS: dict[str, Callable] = {}

_Class = type[object]


def dispatcher_plugin(name) -> Callable:
    """Decorator to register a dispatcher plugin."""

    def decorator(cls: _Class) -> _Class:
        DISPATCHER_PLUGINS[name] = cls
        return cls

    return decorator


# Final
