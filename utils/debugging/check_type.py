from dataclasses import dataclass

from ...src.ota_installer.log_setup import logger


@dataclass(frozen=True, slots=True)
class TypeChecker(object):
    """Represents an object type checker."""

    name: str
    object_to_check: object


def display_type_information(type_checker: TypeChecker) -> None:
    object_type: type = type(type_checker.object_to_check)
    title = type_checker.name.title()
    _object = type_checker.object_to_check
    object_name = object_type.__name__

    if _object is not None:
        print(f'{title}: "{_object}" is a {object_name}')
    else:
        logger.error(f"{title}: Object is None")


if __name__ == "__main__":
    type_checker = TypeChecker(name="example", object_to_check=123)
    display_type_information(type_checker)
