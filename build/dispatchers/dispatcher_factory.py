from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate

import build.dispatchers.types as dispatcher_types


class DispatcherFactory:
    @property
    def dispatcher_collection(self) -> dict[str, type]:
        return {
            "task_group": dispatcher_types.TaskGroupTypeDispatcher,
            "file": dispatcher_types.FileTypeDispatcher,
            "variable": dispatcher_types.VariableTypeDispatcher,
            "directory": dispatcher_types.DirectoryTypeDispatcher,
            "image": dispatcher_types.ImageTypeDispatcher,
        }

    def create_dispatcher(self, dispatcher_type: str, obj: Any) -> DispatcherTemplate:
        dispatcher_class = self.dispatcher_collection.get(dispatcher_type)
        if dispatcher_class:
            return dispatcher_class(obj)
        else:
            raise ValueError(f"Unknown dispatcher type: {dispatcher_type}")
