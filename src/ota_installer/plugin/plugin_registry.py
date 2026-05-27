# src/ota_installer/plugin/plugin_registry.py
from collections.abc import Callable

ClassType = type[object] | None


class PluginRegistry:
    def __init__(self) -> None:
        self.plugins: dict[str, type[object]] = {}

    def register_plugin(self, name):
        def decorator(cls):
            if name in self.plugins:
                raise ValueError(f"Plugin '{name}' already registered")

            self.plugins[name] = cls
            return cls

        return decorator

    def get(self, name: str) -> ClassType:
        key = name.lower().strip()
        return self.plugins.get(key)

    def __contains__(self, name: str) -> bool:
        key = name.lower().strip()
        return key in self.plugins

    def __getitem__(self, name: str) -> ClassType:
        key = name.lower().strip()
        return self.plugins.get(key)


DISPATCHER_PLUGINS = PluginRegistry()
TASK_PLUGINS = PluginRegistry()


def dispatcher_plugin(name: str) -> Callable:
    """Decorator to register a dispatcher plugin."""

    return DISPATCHER_PLUGINS.register_plugin(name)


def task_plugin(name: str) -> Callable:
    """Decorator to register a task plugin."""

    return TASK_PLUGINS.register_plugin(name)


# Signed off by Brian Sanford on 20260523
