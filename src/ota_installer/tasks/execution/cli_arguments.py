from dataclasses import dataclass
from pathlib import Path


@dataclass
class CLIArguments(object):
    """Represents command-line arguments for the application."""

    path: Path
    task_group: str | None = None
    list: bool = False
    version = False


