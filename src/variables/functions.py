from pathlib import Path

from src.structures import FileNameParser
from src.tasks import image_handler


def set_log_file(file_name_bits: FileNameParser) -> str:
    device = file_name_bits.device
    version = file_name_bits.version
    return f"/tmp/ota_variables_{device}_{version}.txt"


def parse_file_name(path):
    return FileNameParser(path)  # .set_raw_name(path).parse_file_name())


def get_image_path(device_name) -> Path:
    return image_handler(device_name)


def set_variable_manager(path: Path) -> "VariableManager":  # type: ignore[return-value]
    from src.variables import VariableManager

    return VariableManager(path)
