# src/ota_installer/program_versioning/containers/software_container_builder.py
from ..constants.software_constants import SoftwareType
from ..containers.software_container import SoftwareContainer


def build_software_container() -> SoftwareContainer:
    """Creates a SoftwareContainer instance with versioning information."""
    return SoftwareContainer(
        title=SoftwareType.TITLE.value,
        major_number=SoftwareType.MAJOR_NUMBER.value,
        minor_number=SoftwareType.MINOR_NUMBER.value,
        patch_number=SoftwareType.PATCH_NUMBER.value,
    )
