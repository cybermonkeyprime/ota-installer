# src/ota_installer/dispatchers/factories/dispatcher_factory.py
from enum import Enum

import src.ota_installer.dispatchers.types as dispatcher_types

DispatcherTypes = (
    dispatcher_types.DirectoryTypeDispatcher
    | dispatcher_types.FileTypeDispatcher
    | dispatcher_types.ImageTypeDispatcher
    | dispatcher_types.TaskGroupTypeDispatcher
    | dispatcher_types.VariableTypeDispatcher
)


class DispatcherFactory(object):
    def create_dispatcher(
        self, dispatcher_type: str, obj: type
    ) -> DispatcherTypes:
        dispatcher_class = DispatcherFactoryMapping[dispatcher_type.upper()]
        return dispatcher_class.value(obj)


class DispatcherFactoryMapping(Enum):
    FILE = dispatcher_types.FileTypeDispatcher
    DIRECTORY = dispatcher_types.DirectoryTypeDispatcher
    IMAGE = dispatcher_types.ImageTypeDispatcher
    TASK_GROUP = dispatcher_types.TaskGroupTypeDispatcher
    VARIABLE = dispatcher_types.VariableTypeDispatcher
