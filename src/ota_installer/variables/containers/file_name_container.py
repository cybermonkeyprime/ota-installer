# src/ota_installer/variables/containers/file_name_container.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileNameContainer(object):
    """Container for file name components."""

    device: str
    pkg_type: str
    build_id: str  # contains [0-9|\.]
    signature: str | None = None


def parse_file_name(raw_name: Path) -> "FileNameContainer":
    """Parse the raw file name into its components."""

    build_structure = Path(raw_name).stem.split("-")
    device, pkg_type, build_id, *signature = build_structure
    return FileNameContainer(
        device=device,
        pkg_type=pkg_type,
        build_id=build_id,
        signature="".join(signature),
    )


def is_base_global(build_id: str) -> bool:
    return not any(char.isalpha() for char in build_id.split(".")[-1])
