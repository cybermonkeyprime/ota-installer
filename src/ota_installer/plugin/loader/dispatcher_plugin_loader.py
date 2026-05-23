# src/ota_installer/plugin/loader/dispatcher_plugin_loader.py
from ...directory.directory_handler import (
    DirectoryDispatcher,
)
from ...image.boot_image_handler import (
    ImageTypeDispatcher,
)
from ...image.generic_image_handler import (
    FileTypeDispatcher,
)
from ...task.task_group_handler import (
    TaskGroupTypeDispatcher,
)
from ...variable.variable_handler import (
    VariableTypeDispatcher,
)
# Signed off by Brian Sanford on 20260523
