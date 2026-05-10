# src/ota_installer/dispatchers/constants/dispatcher_mapping.py
from ..directory_handler import (
    DirectoryDispatcher,
)
from ..images.boot_image_handler import (
    ImageTypeDispatcher,
)
from ..images.generic_image_handler import (
    FileTypeDispatcher,
)
from ..task_group_handler import (
    TaskGroupTypeDispatcher,
)
from ..variables.variable_handler import (
    VariableTypeDispatcher,
)

DispatcherTypes = (
    DirectoryDispatcher
    | FileTypeDispatcher
    | ImageTypeDispatcher
    | TaskGroupTypeDispatcher
    | VariableTypeDispatcher
)
# Signed off by Brian Sanford on 20260318
