# src/ota_installer/tasks/plugin_registry.py

DISPATCHER_PLUGINS = {}


def dispatcher_plugin(name):
    def decorator(cls):
        DISPATCHER_PLUGINS[name] = cls
        return cls

    return decorator
