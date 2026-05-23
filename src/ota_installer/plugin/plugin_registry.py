from collections.abc import Callable

DISPATCHER_PLUGINS: dict[str, Callable] = {}
TASK_PLUGINS: dict[str, Callable] = {}

ClassType = type[object]


def dispatcher_plugin(name: str) -> Callable:
    """Decorator to register a dispatcher plugin."""

    return register_plugin(DISPATCHER_PLUGINS, name)


def task_plugin(name: str) -> Callable:
    """Decorator to register a task plugin."""

    return register_plugin(TASK_PLUGINS, name)


def register_plugin(plugin_dict: dict[str, Callable], name: str) -> Callable:
    """Decorator to register a plugin in the given dictionary."""

    def decorator(cls: ClassType) -> ClassType:
        if name in plugin_dict:
            raise ValueError(f"Plugin '{name}' already registered")

        plugin_dict[name] = cls
        return cls

    return decorator
