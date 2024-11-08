from dataclasses import dataclass


@dataclass
class BaseVersion(object):
    title: str = "OTA-Installer"
    build_number: int = 20241107
    revision_number: int = 10070620
