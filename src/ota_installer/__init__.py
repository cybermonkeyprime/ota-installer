from .versioning.version_config import SoftwareVersion

version = SoftwareVersion
__version__ = SoftwareVersion.version()
