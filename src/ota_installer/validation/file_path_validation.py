# src/ota_installer/validation/file_path_validation.py
from pathlib import Path

from ..log_setup import logger


def file_path_validator(file_path: Path | str) -> Path | None:
    """Validates the given file path against the expected filename pattern."""
    file_path = Path(file_path)

    try:
        _check_file_exists(file_path)
        _check_is_file(file_path)
        _check_file_extension(file_path)

        return file_path.resolve()
    except (FileNotFoundError, ValueError) as err:
        logger.error(f"file_path_validator(): {err}")


def _check_file_exists(file_path: Path) -> None:
    """Checks if the file exists."""
    if not file_path.exists():
        raise FileNotFoundError("File path not found.")


def _check_is_file(file_path: Path) -> None:
    """Checks if the path is a file."""
    if not file_path.is_file():
        raise ValueError(f"Expected a file, got directory: {file_path}")


def _check_file_extension(file_path: Path) -> None:
    """Checks if the file has the correct extension."""
    if file_path.suffix.lower() != ".zip":
        raise ValueError(f"Expected a .zip file, got: {file_path.suffix}")


def main():
    file_path_validator(Path.cwd() / "Bob.txt")


if __name__ == "__main__":
    main()

# Signed off by Brian Sanford on 20260209
