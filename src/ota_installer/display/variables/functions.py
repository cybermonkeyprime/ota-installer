# src/ota_installer/display/variables/functions.py
from ...variables.variable_manager import VariableManager
from ..variables.processors.directory_iteration_processor import (
    DirectoryIterationProcessor,
)
from ..variables.processors.file_iteration_processor import (
    FileIterationProcessor,
)
from ..variables.processors.file_processor import VariableFileProcessor

# Directory names


def set_ota_file_directory(
    processing_function: VariableManager,
) -> None:
    """Sets the OTA file directory in the processing function."""
    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_directory")
        .set_value("path.parent")
        .process_items()
    )


def set_magisk_image_directories(
    processing_function: VariableManager,
) -> None:
    """Sets the Magisk image directories in the processing function."""
    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("local", "remote"))
        .set_directory_type("magisk")
        .set_variable_prefix("_")
        .process_items()
    )


def set_boot_image_directories(
    processing_function: VariableManager,
) -> None:
    """Sets the boot image directories in the processing function."""
    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("stock", "magisk"))
        .set_directory_type("")
        .set_variable_prefix("")
        .process_items()
    )


# File names


def set_ota_file_name(processing_function: VariableManager) -> None:
    """Sets the OTA file name in the processing function."""
    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_name")
        .set_value("path.name")
        .process_items()
    )


def set_image_file_names(
    processing_function: VariableManager,
) -> None:
    """Sets the image file names in the processing function."""
    (
        FileIterationProcessor(processing_function)
        .set_file_names(("payload", "stock", "magisk"))
        .process_items()
    )


# Log files


def set_log_file(processing_function: VariableManager) -> None:
    """Sets the log file in the processing function."""
    (
        VariableFileProcessor(processing_function)
        .set_title("log_file")
        .set_value("log_file")
        .process_items()
    )


# Signed off by Brian Sanford on 20260213
