# src/ota_installer/dispatchers/plugin_loader.py
from ..directory_handler import (
    DirectoryDispatcher,
)
from ..images.boot_image_handler import (
    ImageTypeDispatcher,
)
from ..images.generic_image_handler import (
    FileTypeDispatcher,
)
from ..task_groups.dispatchers.task_group_type_dispatcher import (
    TaskGroupTypeDispatcher,
)
from ..variables.dispatchers.variable_type_dispatcher import (
    VariableTypeDispatcher,
)
# Final
