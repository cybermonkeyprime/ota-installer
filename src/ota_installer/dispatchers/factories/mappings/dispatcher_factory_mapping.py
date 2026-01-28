# src/ota_installer/dispatchers/constants/dispatcher_mapping.py
from enum import Enum

from ....directory.dispatchers.directory_dispatcher import (
    DirectoryDispatcher,
)
from ....images.boot_image.dispatchers.boot_image_dispatcher import (
    ImageTypeDispatcher,
)
from ....images.file_image.dispatchers.file_type_dispatcher import (
    FileTypeDispatcher,
)
from ....task_groups.dispatchers.task_group_type_dispatcher import (
    TaskGroupTypeDispatcher,
)
from ....variables.dispatchers.variable_type_dispatcher import (
    VariableTypeDispatcher,
)


class DispatcherType(Enum):
    """Mapping of dispatcher types to their corresponding classes."""

    FILE = FileTypeDispatcher
    DIRECTORY = DirectoryDispatcher
    IMAGE = ImageTypeDispatcher
    TASK_GROUP = TaskGroupTypeDispatcher
    VARIABLE = VariableTypeDispatcher


DispatcherClasses = (
    DirectoryDispatcher
    | FileTypeDispatcher
    | ImageTypeDispatcher
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)
# Signed off by Brian Sanford on 20260127
