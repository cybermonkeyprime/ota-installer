# src/ota_installer/dispatchers/factories/dispatcher_factory.py
from enum import Enum

from ...directory.dispatchers.directory_dispatcher import (
    DirectoryDispatcher,
)
from ...dispatchers.types.variable_type_dispatcher import (
    VariableTypeDispatcher,
)
from ...images.boot_image.dispatchers.boot_image_dispatcher import (
    ImageTypeDispatcher,
)
from ...images.file_image.dispatchers.file_type_dispatcher import (
    FileTypeDispatcher,
)
from ...task_groups.dispatchers.task_group_type_dispatcher import (
    TaskGroupTypeDispatcher,
)

DispatcherTypes = (
    DirectoryDispatcher
    | FileTypeDispatcher
    | ImageTypeDispatcher
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)


def dispatch_creator(dispatcher_type: str, obj: type) -> DispatcherTypes:
    dispatcher_class = DispatcherFactoryMapping[dispatcher_type.upper()]
    return dispatcher_class.value(obj)


class DispatcherFactoryMapping(Enum):
    FILE = FileTypeDispatcher
    DIRECTORY = DirectoryDispatcher
    IMAGE = ImageTypeDispatcher
    TASK_GROUP = TaskGroupTypeDispatcher
    VARIABLE = VariableTypeDispatcher
