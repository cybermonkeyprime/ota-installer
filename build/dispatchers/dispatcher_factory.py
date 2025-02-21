from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate

from build.dispatchers.types import (
    ImageTypeDispatcher,
    DirectoryTypeDispatcher,
    FileTypeDispatcher,
    TaskGroupTypeDispatcher,
    VariableTypeDispatcher,
)


class DispatcherFactory:
    def create_dispatcher(self, dispatcher_type: str, obj: Any) -> DispatcherTemplate:
        dispatcher_classes = {
            "task_group": TaskGroupTypeDispatcher,
            "file": FileTypeDispatcher,
            "variable": VariableTypeDispatcher,
            "directory": DirectoryTypeDispatcher,
            "image": ImageTypeDispatcher,
        }
        dispatcher_class = dispatcher_classes.get(dispatcher_type)
        if dispatcher_class:
            return dispatcher_class(obj)
        else:
            raise ValueError(f"Unknown dispatcher type: {dispatcher_type}")
