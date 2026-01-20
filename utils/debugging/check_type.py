from collections import namedtuple

from ...src.ota_installer.log_setup import logger

TypeChecker = namedtuple("TypeChecker", ["name", "object_to_check"])


def display_type_information(type_checker: TypeChecker) -> None:
    try:
        object_type: type = type(type_checker.object_to_check)
        title = type_checker.name.title()
        _object = type_checker.object_to_check
        object_name = object_type.__name__
        print(f'{title}: "{_object}" is a {object_name}')
    except Exception as error:
        logger.error(f"{type_checker.name.title()}: {error}")


if __name__ == "__main__":
    type_checker = TypeChecker(name="example", object_to_check=123)
    print(f"{display_type_information(type_checker)}")

# Signed off by Brian Sanford on 20260120
