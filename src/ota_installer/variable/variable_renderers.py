# src/ota_installer/variable/variable_renderers.py
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

from .variable_invocations import DirectoryNameInvocation, FileNameInvocation

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class FilePathRenderer:
    """Container for file paths used in the OTA installer."""

    parts: FilePartContainer
    stock: str | None = None
    magisk: str | None = None
    payload: str | None = None

    def __iter__(self):
        return iter(self.__dict__.items())

    def __post_init__(self) -> None:
        self.image_pipeline()

    @property
    def magisk_image_name(self) -> str:
        return "place_holder"

    @property
    def image_data(self) -> "ImageData":
        from ..image.image_containers import ImageData

        return ImageData(self.parts.device, self.parts.build_id)

    @property
    def log_file(self) -> Path:
        """Generate a log file path based on device and version."""
        from tempfile import gettempdir

        return (
            Path(gettempdir())
            / f"ota-installer_{self.parts.device}_{self.parts.build_id}.txt"
        )

    def image_pipeline(self) -> None:
        from ..image.image_name import ImageName

        for key in ImageName.valid_members():
            value = self.image_data(ImageName[key])
            object.__setattr__(self, key.lower(), value)


@dataclass(frozen=True, slots=True)
class FilePartRenderer:
    """Container for variable types used in OTA installation."""

    file_path: Path

    @property
    def file_parts(self) -> FilePartContainer:
        """Parse the raw file name into its components."""

        from parse import parse

        FILENAME_PATTERN = "{device}-{pkg_type}-{build_id}-{signature}"

        filename_stem = self.file_path.stem

        result = parse(FILENAME_PATTERN, filename_stem)

        if result is None:
            message = f"Invalid OTA filename: {filename_stem!r}"
            raise ValueError(message)

        return FilePartContainer(**result.named)


@dataclass(frozen=True, slots=True)
class FilePartContainer:
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


@dataclass(frozen=True)
class VariableRenderer(Generic[T]):
    class_type: type[T]

    def __call__(self, **arguments: Any) -> T:
        return self.class_type(**arguments)


class VariableType(Enum):
    CONTEXT = VariableRenderer(FilePartRenderer)
    FILE_NAME = VariableRenderer(FileNameInvocation)
    FILE_PATH = VariableRenderer(FilePathRenderer)
    DIRECTORY = VariableRenderer(DirectoryNameInvocation)

    def build(self, **kwargs: Any) -> Any:
        return self.value(**kwargs)


# Signed off by Brian Sanford on 20260902
