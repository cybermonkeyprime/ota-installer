# src/ota_installer/dispatchers/constants/dispatcher_mapping.py
from enum import Enum

from ...directory.dispatchers.directory_dispatcher import (
    DirectoryDispatcher,
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
from ...variables.dispatchers.variable_type_dispatcher import (
    VariableTypeDispatcher,
)


class DispatcherFactoryMapping(Enum):
    """Enumeration of dispatcher types."""

    FILE = FileTypeDispatcher
    DIRECTORY = DirectoryDispatcher
    IMAGE = ImageTypeDispatcher
    TASK_GROUP = TaskGroupTypeDispatcher
    VARIABLE = VariableTypeDispatcher


DispatcherTypes = (
    DirectoryDispatcher
    | FileTypeDispatcher
    | ImageTypeDispatcher
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)
# Signed off by Brian Sanford on 20260118
