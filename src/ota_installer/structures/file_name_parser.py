# src/ota_installer/structures/file_name_parser.py
from collections import namedtuple
from pathlib import Path

FileNameContainer = namedtuple(
    "FileNameParts", ["device", "file_type", "version", "extra"]
)


def parse_file_name(raw_name: Path) -> tuple:
    parts = Path(raw_name).stem.split("-")
    device, file_type, version, *extra_parts = parts
    return FileNameContainer(
        device=device,
        file_type=file_type,
        version=version,
        extra=extra_parts,
    )


if __name__ == "__main__":
    file_name = Path("device-type-version-extra-info")
    parse_file_name(file_name)  # .set_raw_name(file_name).parse_file_name()
