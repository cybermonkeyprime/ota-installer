# src/ota_installer/variable/variable_info.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=False, slots=True)
class MagiskPathInvocation:
    """Represents the local and remote directory paths."""

    local_path: Path
    remote_path: Path


@dataclass(frozen=True, slots=True)
class DirectoryNameInvocation:
    """Container for directory names used in the OTA installer."""

    magisk: MagiskPathInvocation

    def __iter__(self):
        return iter(self.__dict__.items())


@dataclass(frozen=True, slots=True)
class FileNameInvocation:
    """Represents information about a file name."""

    path: Path
    parts: FilePartInvocation

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def device(self) -> str:
        return self.parts.device


@dataclass(frozen=True, slots=True)
class FilePartInvocation:
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


# Signed off by Brian Sanford on 20260712
