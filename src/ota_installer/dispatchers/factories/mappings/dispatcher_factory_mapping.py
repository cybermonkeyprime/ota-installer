# src/ota_installer/dispatchers/constants/dispatcher_mapping.py
from enum import Enum

from ....directory.dispatchers.directory_dispatcher import (
    DirectoryDispatcher,
)

# from ....images.boot_image.dispatchers.boot_image_dispatcher import (
#    ImageTypeDispatcher,
# )
from ....images.boot_image.constants.boot_image_type import BootImageType
from ....images.file_image.dispatchers.file_type_dispatcher import (
    FileTypeDispatcher,
)
from ....task_groups.dispatchers.task_group_type_dispatcher import (
    TaskGroupTypeDispatcher,
)
from ....variables.dispatchers.variable_type_dispatcher import (
    VariableTypeDispatcher,
)

DispatcherClasses = (
    DirectoryDispatcher
    | FileTypeDispatcher
    | BootImageType
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)


class DispatcherType(Enum):
    """Mapping of dispatcher types to their corresponding classes."""

    FILE = FileTypeDispatcher
    DIRECTORY = DirectoryDispatcher
    IMAGE = BootImageType
    TASK_GROUP = TaskGroupTypeDispatcher
    VARIABLE = VariableTypeDispatcher

    @classmethod
    def allowed_dispatchers(cls) -> tuple[str, ...]:
        """Returns a tuple of allowed dispatcher names."""
        search = tuple(enum_member.name for enum_member in cls)
        return search


# Signed off by Brian Sanford on 20260317
