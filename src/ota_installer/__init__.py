from .handler.version_handler import SoftwareVersion

version = SoftwareVersion
__version__ = f"{version.MAJOR_NUMBER.value}.{version.MINOR_NUMBER.value}.{version.PATCH_NUMBER.value}"
