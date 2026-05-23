from collections.abc import Callable

DISPATCHER_PLUGINS: dict[str, Callable] = {}
TASK_PLUGINS: dict[str, Callable] = {}

_Class = type[object]


def dispatcher_plugin(name) -> Callable:
    """Decorator to register a dispatcher plugin."""

    def decorator(cls: _Class) -> _Class:
        if name in DISPATCHER_PLUGINS:
            raise ValueError(f"Dispatcher Plugin '{name}' already registered")

        DISPATCHER_PLUGINS[name] = cls

        return cls

    return decorator


def task_plugin(name: str) -> Callable:
    """Decorator to register a task plugin."""

    def decorator(cls: _Class) -> _Class:
        if name in TASK_PLUGINS:
            raise ValueError(f"Task Plugin '{name}' already registered")

        TASK_PLUGINS[name] = cls

        return cls

    return decorator
