# src/ota_installer/validation/validate_zip_file.py
from pathlib import Path
from zipfile import ZipFile, is_zipfile

import magic

from ..log_setup import log_status


class InvalidZipFileError(ValueError):
    pass


class EmptyZipFileError(BaseException):
    pass


VALID_ZIP_MIME_TYPES: set[str] = {"application/java-archive"}


def validate_ota_package(path: str | Path) -> Path | None:
    zip_path = Path(path)

    if not zip_path.exists():
        log_status(
            "Critical", FileNotFoundError, f"Path does not exist: {zip_path}"
        )

    if not zip_path.is_file():
        log_status("Critical", FileExistsError, f"Not a file: {zip_path}")

    mime = magic.from_file(filename=str(object=path), mime=True)

    if mime not in VALID_ZIP_MIME_TYPES:
        log_status("Critical", None, f"Unexpected MIME type: {mime}")

    if not is_zipfile(filename=zip_path):
        log_status(
            "Critical", InvalidZipFileError, "Not a valid zip file format!"
        )

    if not ZipFile(zip_path).namelist():
        log_status("Critical", None, "Zip archive is empty.")

    return zip_path.resolve()


# Signed off by Brian Sanford on 20260625
