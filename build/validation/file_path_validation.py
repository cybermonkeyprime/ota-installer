import sys
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import ValidationError

import build.validation as validation


@dataclass
class FilePathValidation(object):
    """Creates a directory based on the given path."""

    file_path: Path = field(default_factory=Path)

    def validator(self) -> Path:
        try:
            file_existence_model = validation.FileExistenceModel(
                file_path=self.file_path
            )
            file_existence_model.checker()
        except ValidationError:
            print(f"Warning, {Path(self.file_path).stem} does not exist.")
            sys.exit()
        finally:
            return Path(self.file_path)
