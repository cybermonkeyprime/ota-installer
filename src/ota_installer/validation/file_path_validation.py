# src/ota_installer/validation/file_path_validation.py
from pathlib import Path

from ..log_setup import logger


def file_path_validator(file_path: Path | str) -> Path | None:
    """Validates the given file path against the expected filename pattern."""
    file_path = Path(file_path)

    if not _file_exists(file_path):
        logger.error("File path not found.")
        return None

    if not _is_file(file_path):
        logger.error(f"Expected a file, got directory: {file_path}")
        return None

    if not _has_correct_extension(file_path):
        logger.error(f"Expected a .zip file, got: {file_path.suffix}")
        return None

    return file_path.resolve()


def _file_exists(file_path: Path) -> bool:
    """Checks if the file exists."""
    return file_path.exists()


def _is_file(file_path: Path) -> bool:
    """Checks if the path is a file."""
    return file_path.is_file()


def _has_correct_extension(file_path: Path) -> bool:
    """Checks if the file has the correct extension."""
    return file_path.suffix.lower() == ".zip"


def main():
    file_path_validator(Path.cwd() / "Bob.txt")


if __name__ == "__main__":
    main()

