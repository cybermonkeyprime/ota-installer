# src/ota_installer/dispatchers/factories/dispatcher_factory.py
from enum import Enum

from ...dispatchers.types import (
    DirectoryTypeDispatcher,
    FileTypeDispatcher,
    ImageTypeDispatcher,
    TaskGroupTypeDispatcher,
    VariableTypeDispatcher,
)

DispatcherTypes = (
    DirectoryTypeDispatcher
    | FileTypeDispatcher
    | ImageTypeDispatcher
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)


class DispatcherFactory(object):
    def create_dispatcher(
        self, dispatcher_type: str, obj: type
    ) -> DispatcherTypes:
        dispatcher_class = DispatcherFactoryMapping[dispatcher_type.upper()]
        return dispatcher_class.value(obj)


class DispatcherFactoryMapping(Enum):
    FILE = FileTypeDispatcher
    DIRECTORY = DirectoryTypeDispatcher
    IMAGE = ImageTypeDispatcher
    TASK_GROUP = TaskGroupTypeDispatcher
    VARIABLE = VariableTypeDispatcher
