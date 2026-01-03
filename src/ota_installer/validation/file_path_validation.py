# src/ota_installer/validation/file_path_validation.py
import re
from pathlib import Path

from ..log_setup import logger

FILENAME_PATTERN = re.compile(
    r"(?P<build>[a-z0-9-]+)\."
    r"(?P<date>\d{6})\."
    r"(?P<version>[\d.]+)\."
    r"(?P<revision>[a-z0-9]+)-"
    r"(?P<hash>[a-f0-9]+)\.zip"
)


def file_path_validator(file_path: Path | str) -> Path | None:
    file_path = Path(file_path)
    file_path_string = str(file_path.name)

    try:
        if not FILENAME_PATTERN.match(file_path_string):
            raise ValueError(f"Invalid filename format: {file_path_string}")
        if not file_path.exists():
            raise FileNotFoundError("file_path not found")
        if not file_path.is_file():
            raise ValueError(f"Expected a file, got directory: {file_path}")
        if file_path.suffix.lower() != ".zip":
            raise ValueError(f"Expected a .zip file, got: {file_path.suffix}")

        return file_path.resolve()
    except (FileNotFoundError, ValueError) as err:
        logger.error(f"file_path_validator(): {err}")


def main():
    file_path_validator(Path.cwd() / "Bob.txt")


if __name__ == "__main__":
    main()
