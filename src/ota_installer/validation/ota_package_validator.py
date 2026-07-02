# src/ota_installer/validation/validate_zip_file.py
from pathlib import Path
from zipfile import ZipFile, is_zipfile

import magic

from ..log_setup import logger


class InvalidZipFileError(ValueError):
    pass


VALID_ZIP_MIME_TYPES: set[str] = {"application/java-archive"}


def validate_ota_package(path: str | Path) -> Path | None:
    zip_path = Path(path)

    if not zip_path.exists():
        message = f"Path does not exist: {zip_path}"
        report = {"status": "Error", "reason": message}
        logger.critical(message)
        return None

    if not zip_path.is_file():
        message = f"Not a file: {zip_path}"
        report = {"status": "Error", "reason": message}
        logger.critical(message)
        return None

    mime = magic.from_file(filename=str(object=path), mime=True)

    if mime not in VALID_ZIP_MIME_TYPES:
        message = f"Unexpected MIME type: {mime}"
        report = {"status": "Error", "reason": message}
        logger.critical(message)
        return None

    if not is_zipfile(filename=zip_path):
        message = "Not a valid zip file format!"
        report = {"status": "Error", "reason": message}
        logger.critical(message)
        return None

    if not ZipFile(zip_path).namelist():
        message = "Zip archive is empty."
        report = {"status": "Error", "reason": message}
        logger.critical(message)
        return None

    return zip_path.resolve()


# Signed off by Brian Sanford on 20260625
