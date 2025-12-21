# src/ota_installer/tasks/plugin_registry.py

TASK_PLUGINS = {}


def task_plugin(name):
    def decorator(cls):
        TASK_PLUGINS[name] = cls
        return cls

    return decorator
