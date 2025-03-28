from dataclasses import dataclass, field
from typing import Any

import build.structures as structures


@dataclass
class LogFileManager(object):
    """Generates a log file name based on the file name parser."""

    parser: Any = field(default_factory=lambda: structures.FileNameParser)

    def __str__(self) -> str:
        return f"/tmp/ota_variables_{self.parser.device}_{self.parser.version}.txt"
