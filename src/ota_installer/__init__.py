from .versioning.version_info import SoftwareVersion

version = SoftwareVersion
__version__ = (
    f"{version.MAJOR_NUMBER.value}."
    f"{version.MINOR_NUMBER.value}."
    f"{version.PATCH_NUMBER.value}"
)
