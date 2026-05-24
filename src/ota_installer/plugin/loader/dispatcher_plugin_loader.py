# src/ota_installer/plugin/loader/dispatcher_plugin_loader.py
from ...handler.directory_handler import (
    DirectoryDispatcher,
)
from ...handler.image.boot_image_handler import (
    ImageTypeDispatcher,
)
from ...handler.image.generic_image_handler import (
    FileTypeDispatcher,
)
from ...task.task_group_handler import (
    TaskGroupTypeDispatcher,
)
from ...handler.variable_handler import (
    VariableTypeDispatcher,
)
# Signed off by Brian Sanford on 20260523
