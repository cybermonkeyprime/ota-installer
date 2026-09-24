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


def pipeline_step(func):
    func.is_step = True
    return func


@dataclass(frozen=True, slots=True)
class OTAPackageValidator:
    zip_path: Path
    valid_zip_mime_types: set[str] = {"application/java-archive"}

    @pipeline_step
    def does_path_exist(self) -> None:
        if not self.zip_path.exists():
            LogType.CRITICAL.raise_error(
                FileNotFoundError, f"Path does not exist: {self.zip_path}"
            )

    @pipeline_step
    def is_path_a_zip_file(self) -> None:
        if not self.zip_path.is_file():
            LogType.CRITICAL.raise_error(
                FileExistsError, f"Not a file: {self.zip_path}"
            )

    @pipeline_step
    def is_mime_type_correct(self) -> None:
        mime = magic.from_file(filename=str(object=self.zip_path), mime=True)

        if mime not in self.valid_zip_mime_types:
            LogType.CRITICAL.raise_error(
                ValueError, f"Unexpected MIME type: {mime}"
            )

    @pipeline_step
    def is_a_zipfile(self) -> None:
        if not is_zipfile(filename=self.zip_path):
            LogType.CRITICAL.raise_error(
                InvalidZipFileError, "Not a valid zip file format!"
            )

    @pipeline_step
    def is_archive_empty(self) -> None:
        if not ZipFile(self.zip_path).namelist():
            LogType.CRITICAL.raise_error(
                EmptyZipFileError, "Zip archive is empty."
            )


PIPELINE_STEPS = tuple(
    name
    for name, func in OTAPackageValidator.__dict__.items()
    if getattr(func, "is_step", False)
)


def validate_ota_package(path: str | Path) -> Path:
    zip_path = Path(path)

    pipeline = OTAPackageValidator(zip_path)

    for step_name in PIPELINE_STEPS:
        method = getattr(pipeline, step_name)
        method()  # Execute the pipeline step

    return zip_path.resolve()


# Signed off by Brian Sanford on 20260924
