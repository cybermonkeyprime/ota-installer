import sys


def import_filter(importer: str, name: str, fromlist: tuple[str, ...]) -> bool:
    """
    Python 3.15 Runtime Import Filter (PEP 810).
    Returns True to defer/lazy-load; False to force immediate eager execution.
    """
    if name and (name.endswith("plugin.loader") or "plugin" in name):
        return False  # Force immediate eager load to execute registration code

    MUST_BE_EAGER = {
        "typer",
        "loguru",
        "dependency_injector",
    }

    root_package = name.split(".")[0] if name else ""
    return root_package not in MUST_BE_EAGER


# Configure the runtime before executing application code
if hasattr(sys, "set_lazy_imports_filter"):
    sys.set_lazy_imports_filter(import_filter)  # type: ignore
    sys.set_lazy_imports("all")  # type: ignore

# --- ORIGINAL MAIN CODE PATH STARTS HERE ---
from .command_line_interface import cli

# DO NOT REMOVE, PLUGIN LOADERS!!!
# Because of our filter, this line forces eager execution immediately!
from .plugin.loader import dispatcher_plugin_loader, task_plugin_loader


def main() -> None:
    """Entry point for the application.

    Initializes the command line interface.
    """
    cli()


if __name__ == "__main__":
    main()
