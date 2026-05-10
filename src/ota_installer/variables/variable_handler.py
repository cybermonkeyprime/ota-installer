# variables/variable_handler.py
from dataclasses import dataclass, field
from pathlib import Path

from ..dispatchers.dispatcher_handler import DispatcherTemplate
from ..dispatchers.dispatcher_type import DispatcherType
from ..dispatchers.plugins.dispatcher_plugin_registry import dispatcher_plugin
from .variable_info import FileNameContainer

StrPathDict = dict[str, Path | str]


def parse_file_name(raw_name: Path) -> "FileNameContainer":
    """Parse the raw file name into its components."""

    build_structure: list[str] = Path(raw_name).stem.split(sep="-")
    device, pkg_type, build_id, *signature = build_structure
    return FileNameContainer(
        device=device,
        pkg_type=pkg_type,
        build_id=build_id,
        signature="".join(signature),
    )


def is_base_global(build_id: str) -> bool:
    return not any(char.isalpha() for char in build_id.split(".")[-1])


def set_log_file(file_name_parts: FileNameContainer) -> str:
    """Generate a log file path based on device and version."""
    device = file_name_parts.device
    version = file_name_parts.build_id
    return f"/tmp/ota-installer_{device}_{version}.txt"


def set_variable_manager(path: Path) -> "VariableManager":  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    from ..log_setup import logger
    from ..validation.validate_zip_file import validate_zip_file
    from .variable_manager import VariableManager

    """Create a VariableManager instance after validating the file path. """

    valid_path = validate_zip_file(path)

    if not valid_path:
        logger.error(f"Invalid file path: {path}. Aborting.")
        raise SystemExit()

    return VariableManager(path=valid_path)


def get_file_image_path(name: str, device: str, version) -> Path:
    from ..images.generic_image_handler import (
        FileImageAttributes,
    )

    """Retrieve the file image path based on name, device, and version. """

    return (
        FileImageAttributes[name.upper()]
        .set_device(device)
        .set_version(version)
        .set_file_path()
    )


@dispatcher_plugin(name=DispatcherType.VARIABLE.value)
@dataclass
class VariableTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling variable types."""

    obj: type = field(default_factory=lambda: type)
    collection: StrPathDict = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the collection of paths based on the provided object."""
        self.collection = self._initialize_collection()

    def _initialize_collection(self) -> StrPathDict:
        """Creates a collection of paths and log file."""
        return {
            "path.name": Path(self.obj.path).name,
            "path.parent": Path(self.obj.path).parent,
            "log_file": self.obj.file_paths.log_file,
        }


# Signed off by Brian Sanford on 20260509
