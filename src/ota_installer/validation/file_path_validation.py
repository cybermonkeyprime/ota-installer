# src/ota_installer/validation/file_path_validation.py
from pathlib import Path

from rich.console import Console

console = Console()


def file_path_validator(file_path: Path | str) -> Path:
    file_path = Path(file_path)
    valid_and_exists = file_path.is_file() and file_path.suffix == ".zip"
    if not valid_and_exists:
        console.print(
            f"[yellow]Warning:[/yellow] '{file_path.name}' "
            "is not a valid .zip file or does not exist."
        )
    return file_path


def main():
    file_path_validator(Path.cwd() / "Bob.txt")


if __name__ == "__main__":
    main()
