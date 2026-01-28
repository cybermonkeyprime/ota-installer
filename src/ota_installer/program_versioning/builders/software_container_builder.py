# src/ota_installer/program_versioning/containers/software_container_builder.py
from ..constants.software_constants import SoftwareConstants
from ..containers.software_container import SoftwareContainer


def build_software_container() -> SoftwareContainer:
    """Builds a SoftwareContainer instance with versioning information."""
    return SoftwareContainer(
        title=SoftwareConstants.TITLE.value,
        major_number=SoftwareConstants.MAJOR_NUMBER.value,
        minor_number=SoftwareConstants.MINOR_NUMBER.value,
        patch_number=SoftwareConstants.PATCH_NUMBER.value,
    )


