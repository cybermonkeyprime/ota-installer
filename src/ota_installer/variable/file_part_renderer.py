# src/ota_installer/variable/file_part_renderer.py
from dataclasses import dataclass
from pathlib import Path


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


# Signed off by Brian Sanford on 20260902
