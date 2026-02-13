# src/ota_installer/tasks/plugin_registry.py
from collections.abc import Callable

TASK_PLUGINS: dict[str, Callable] = {}


def task_plugin(name: str) -> Callable:
    """Decorator to register a task plugin."""

    def decorator(cls) -> object:
        if name in TASK_PLUGINS:
            raise ValueError(f"Task Plugin '{name}' already registered")

        TASK_PLUGINS[name] = cls

        return cls

    return decorator


# Signed off by Brian Sanford on 20260213
