# src/ota_installer/validation/file_path_validation.py
from pathlib import Path

from ..log_setup import logger


def file_path_validator(file_path: Path | str) -> Path | None:
    """Validates the given file path against the expected filename pattern."""
    file_path = Path(file_path)

    try:
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
