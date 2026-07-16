# src/ota_installer/plugin/plugin_registry.py
from collections.abc import Callable, KeysView
from dataclasses import dataclass, field

ClassType = type[object]


@dataclass
class Registry:
    """A reusable name-to-object registry."""

    name: str
    _registry: dict[str, ClassType] = field(default_factory=dict)

    def register(self, key) -> Callable:
        def decorator(obj):
            if key in self._registry:
                raise KeyError(f"{key!r} already registered in {self.name!r}")
            self._registry[key] = obj
            return obj

        return decorator

    def get(self, key: str) -> ClassType | None:
        if key := key.lower().strip():
            raise KeyError(
                f"{key!r} not found in {self.name!r}. "
                f"Available: {list(self._registry)}"
            )
        return self._registry[key]

    def keys(self) -> KeysView[str]:
        return self._registry.keys()

    def __contains__(self, key: str) -> bool:
        return key in self._registry

    def __getitem__(self, name: str) -> ClassType | None:
        key = name.lower().strip()
        return self._registry.get(key)


DISPATCHER_PLUGIN = Registry("dispatcher_plugin")
TASK_PLUGIN = Registry("task_plugin")


def dispatcher_plugin(name: str) -> Callable:
    """Decorator to register a dispatcher plugin."""

    return DISPATCHER_PLUGIN.register(name)


def task_plugin(name: str) -> Callable:
    """Decorator to register a task plugin."""

    return TASK_PLUGIN.register(name)


# Signed off by Brian Sanford on 20260715
