# src/ota_installer/plugin/plugin_registry.py
from collections.abc import Callable, KeysView
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar

PluginType = TypeVar("PluginType")
ClassType = type[object]


@dataclass
class Registry:
    """A reusable name-to-object registry."""

    name: str
    _registry: dict[str, ClassType] = field(default_factory=dict)

    def register(
        self,
        key: str,
    ) -> Callable[[PluginType], PluginType]:
        """Return a decorator that registers an object under the given key."""

        normalized_key = key.lower().strip()

        def decorator(obj: PluginType) -> PluginType:
            if normalized_key in self._registry:
                raise KeyError(
                    f"{normalized_key!r} is already registered "
                    f"in {self.name!r}"
                )

            self._registry[normalized_key] = obj
            return obj

        return decorator

    def get(self, key: str) -> ClassType:
        """Return the registered object associated with the given key."""

        normalized_key = key.lower().strip()

        if normalized_key not in self._registry:
            raise KeyError(
                f"{normalized_key!r} not found in {self.name!r}. "
                f"Available: {list(self._registry)}"
            )

        return self._registry[normalized_key]

    def keys(self) -> KeysView[str]:
        """Return a view containing the registered keys."""

        return self._registry.keys()

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, str):
            return False

        return key.lower().strip() in self._registry

    def __getitem__(self, key: str) -> ClassType:
        return self.get(key)


class Plugin(Enum):
    """Available plugin registries."""

    DISPATCHER = Registry("dispatcher_plugin")
    TASK = Registry("task_plugin")

    def register(
        self,
        name: str,
    ) -> Callable[[PluginType], PluginType]:
        """Register an object with this plugin registry."""

        return self.value.register(name)

    def get(self, name: str) -> ClassType:
        """Return a registered plugin."""

        return self.value.get(name)

    def keys(self) -> KeysView[str]:
        """Return the keys registered with this plugin type."""

        return self.value.keys()

    def __contains__(self, name: object) -> bool:
        return name in self.value

    def __getitem__(self, name: str) -> ClassType:
        return self.value[name]


# Signed off by Brian Sanford on 20260715
