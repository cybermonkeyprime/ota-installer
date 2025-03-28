from dataclasses import dataclass, field
from pathlib import Path

import build.structures as structures
import build.validation as validation


@dataclass
class FileNameManager(object):
    path: Path = field(default_factory=Path)

    @property
    def parts(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)

    def validator(self) -> Path:
        file_path_validation = validation.FilePathValidation(file_path=self.path)
        return file_path_validation.validator()

    def parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)
