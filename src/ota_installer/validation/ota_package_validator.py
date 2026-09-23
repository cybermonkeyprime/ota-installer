# src/ota_installer/validation/validate_zip_file.py
from pathlib import Path
from zipfile import ZipFile, is_zipfile

import magic

from ..log_setup import LogType


class InvalidZipFileError(ValueError):
    pass


class EmptyZipFileError(ValueError):
    pass


VALID_ZIP_MIME_TYPES: set[str] = {"application/java-archive"}


def validate_ota_package(path: str | Path) -> Path:
    zip_path = Path(path)

    tests = (
        does_path_exist,
        is_a_zipfile,
        is_mime_type_correct,
        is_a_zipfile,
        is_archive_empty,
    )

    for test in tests:
        test(zip_path)

    return zip_path.resolve()


def does_path_exist(zip_path: Path) -> None:
    if not zip_path.exists():
        LogType.CRITICAL.raise_error(
            FileNotFoundError, f"Path does not exist: {zip_path}"
        )


def is_path_a_zip_file(zip_path: Path) -> None:
    if not zip_path.is_file():
        LogType.CRITICAL.raise_error(
            FileExistsError, f"Not a file: {zip_path}"
        )


def is_mime_type_correct(path: Path) -> None:
    mime = magic.from_file(filename=str(object=path), mime=True)

    if mime not in VALID_ZIP_MIME_TYPES:
        LogType.CRITICAL.raise_error(
            ValueError, f"Unexpected MIME type: {mime}"
        )


def is_a_zipfile(zip_path: Path):
    if not is_zipfile(filename=zip_path):
        LogType.CRITICAL.raise_error(
            InvalidZipFileError, "Not a valid zip file format!"
        )


def is_archive_empty(zip_path: Path):
    if not ZipFile(zip_path).namelist():
        LogType.CRITICAL.raise_error(
            EmptyZipFileError, "Zip archive is empty."
        )


# Signed off by Brian Sanford on 20260923
