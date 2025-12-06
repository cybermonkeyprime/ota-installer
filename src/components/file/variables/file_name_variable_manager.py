from dataclasses import dataclass, field
from pathlib import Path

from src.components.file.structures import FileNameParserStructure
from src.validation import FilePathValidation


@dataclass
class FileNameVariableManager(object):
    """
    A class to manage file names, providing functionality to parse and validate
    file paths.
    """

    path: Path = field(default_factory=Path)

    @property
    def parts(self) -> FileNameParserStructure:
        """Parses the file name from the file path."""

        return self.parser()

    def validator(self) -> Path:
        """Validates the file path."""
        file_path_validation = FilePathValidation(file_path=self.path)
        return file_path_validation.validator()

    def parser(self) -> FileNameParserStructure:
        """Parses the file name from the file path."""
        return FileNameParserStructure(self.path.stem)
