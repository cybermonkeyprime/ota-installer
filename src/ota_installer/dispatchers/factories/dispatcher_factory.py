# src/ota_installer/dispatchers/factories/dispatcher_factory.py
from enum import Enum

from ...dispatchers.types.directory_type_dispatcher import (
    DirectoryTypeDispatcher,
)
from ...dispatchers.types.file_type_dispatcher import (
    FileTypeDispatcher,
)
from ...dispatchers.types.variable_type_dispatcher import (
    VariableTypeDispatcher,
)
from ...images.boot_image.dispatchers.boot_image_dispatcher import (
    ImageTypeDispatcher,
)
from ...task_groups.dispatchers.task_group_type_dispatcher import (
    TaskGroupTypeDispatcher,
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
