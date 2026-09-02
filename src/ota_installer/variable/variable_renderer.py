# src/ota_installer/variable/variable_renderer.py
from dataclasses import dataclass
from enum import Enum
from typing import Any, Generic, TypeVar

from .file_part_renderer import FilePartRenderer
from .file_path_renderer import FilePathRenderer
from .variable_info import DirectoryNames, FileNameInvocation

T = TypeVar("T")


@dataclass(frozen=True)
class VariableRenderer(Generic[T]):
    class_type: type[T]

    def __call__(self, **arguments: Any) -> T:
        return self.class_type(**arguments)


class VariableType(Enum):
    CONTEXT = VariableRenderer(FilePartRenderer)
    FILE_NAME = VariableRenderer(FileNameInvocation)
    FILE_PATH = VariableRenderer(FilePathRenderer)
    DIRECTORY = VariableRenderer(DirectoryNames)

    def build(self, **kwargs: Any) -> Any:
        return self.value(**kwargs)


# src/ota_installer/variable/variable_renderer.py
