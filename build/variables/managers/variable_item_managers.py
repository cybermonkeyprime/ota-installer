from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as type_managers
import build.validation as validation


@dataclass
class BootImageManager(object):
    """Manages boot images by providing file path and related operations.

    Attributes:
        file_path: The path to the boot image file.
        directory_path: The directory where boot images are stored.
    """

    file_path: Path = field(
        default_factory=lambda: Path.home() / "Android" / "boot-images"
    )

    @property
    def file_name_parser(self) -> structures.FileNameParser:
        """Creates a FileNameParser instance for the boot image file."""
        return structures.FileNameParser(self.file_path.stem)

    @property
    def struct(self) -> Optional[definitions.ImageFile]:
        """Attempts to create an ImageFile structure for the boot image."""
        file_manager = type_managers.ImageFile(
            self.file_name_parser, str(self.file_path)
        )
        try:
            return file_manager.create_image()
        except Exception as e:
            print(f"Error creating image file: {e}")
            return None


@dataclass
class DispatcherManager(object):
    """
    Manages the creation of dispatchers for different object types.

    Attributes:
        dispatcher_class: The class to be used for creating dispatcher instances.
        base_path: The base path to be used by the dispatchers.
        allowed_object_types: A set of allowed object types for dispatching.
    """

    dispatcher_class: Callable = field(default_factory=lambda: type)
    base_path: Path = field(default_factory=Path)
    allowed_objects_types: set = field(
        default_factory=lambda: {"directory", "file", "variable"}
    )

    def creator(self, object_type) -> Optional[dispatchers.MainDispatcher]:
        """
        Creates a dispatcher for the given object type if allowed.

        Args:
            object_type: The type of object for which to create a dispatcher.

        Returns:
            An instance of MainDispatcher or None if the object type is not allowed.
        """

        try:
            if object_type in self.allowed_objects_types:
                return dispatchers.MainDispatcher(
                    object_type, self.dispatcher_class(self.base_path)
                )
        except Exception as err:
            print(err)


@dataclass
class FileNameManager(object):
    """
    A class to manage file names, providing functionality to parse and validate
    file paths.

    Attributes:
        file_path (Path): The file path to manage.
    """

    path: Path = field(default_factory=Path)

    @property
    def parts(self) -> structures.FileNameParser:
        """
        Parses the file name from the file path.

        Returns:
            FileNameParser: An instance of FileNameParser with parsed file name.
        """

        return self.parser()

    def validator(self) -> Path:
        """
        Validates the file path.

        Returns:
            Optional[Path]: The validated file path or None if invalid.
        """

        """Validates the file path."""
        file_path_validation = validation.FilePathValidation(file_path=self.path)
        return file_path_validation.validator()

    def parser(self) -> structures.FileNameParser:
        """
        Parses the file name from the file path.

        Returns:
            FileNameParser: An instance of FileNameParser with parsed file name.
        """
        return structures.FileNameParser(self.path.stem)


@dataclass
class LogFileManager(object):
    """
    Generates a log file name based on the file name parser.

    Attributes:
        file_name_parser: An instance of FileNameParser used to parse device
        and version information for the log file name.
    """

    parser: Any = field(default_factory=lambda: structures.FileNameParser)

    def __str__(self) -> str:
        """
        Generates a log file path string.

        Returns:
            A string representing the log file path.
        """

        return f"/tmp/ota_variables_{self.parser.device}_{self.parser.version}.txt"


@dataclass
class PatchedImageManager:
    """
    Manages the details of an image.

    Attributes:
        image_name (str): The name of the image. Defaults to "placeholder".
    """

    image_name: str = field(default="place_holder")
