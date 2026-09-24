# src/ota_installer/validation/validate_zip_file.py
from dataclasses import dataclass
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

    return OTAPackageValidator(zip_path).test_pipeline()


@dataclass(frozen=True, slots=True)
class OTAPackageValidator:
    zip_path: Path

    def does_path_exist(self) -> None:
        if not self.zip_path.exists():
            LogType.CRITICAL.raise_error(
                FileNotFoundError, f"Path does not exist: {self.zip_path}"
            )

    def is_path_a_zip_file(self) -> None:
        if not self.zip_path.is_file():
            LogType.CRITICAL.raise_error(
                FileExistsError, f"Not a file: {self.zip_path}"
            )

    def is_mime_type_correct(self) -> None:
        mime = magic.from_file(filename=str(object=self.zip_path), mime=True)

        if mime not in VALID_ZIP_MIME_TYPES:
            LogType.CRITICAL.raise_error(
                ValueError, f"Unexpected MIME type: {mime}"
            )

    def is_a_zipfile(self) -> None:
        if not is_zipfile(filename=self.zip_path):
            LogType.CRITICAL.raise_error(
                InvalidZipFileError, "Not a valid zip file format!"
            )

    def is_archive_empty(self) -> None:
        if not ZipFile(self.zip_path).namelist():
            LogType.CRITICAL.raise_error(
                EmptyZipFileError, "Zip archive is empty."
            )

    def test_pipeline(self):
        tests = (
            self.does_path_exist,
            self.is_a_zipfile,
            self.is_mime_type_correct,
            self.is_a_zipfile,
            self.is_archive_empty,
        )

        for test in tests:
            test()

        return self.zip_path.resolve()
