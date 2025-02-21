from dataclasses import dataclass


@dataclass
class BaseVersion(object):
    title: str = "OTA-Installer"
    build_number: int = 20250221
    revision_number: int = 2210330
