# src/debugging/object_inspector.py
import inspect
from typing import Self


def inspect_object(object_name: inspect._IntrospectableCallable):
    (
        ObjectInspector()
        .set_object_name(object_name)
        .show_intro()
        .show_type()
        .show_source_code()
        .show_signature()
        .show_doc_strings()
    )


class ObjectInspector(object):
    """An object inspector that shows a report of an object"""

    def set_object_name(
        self, object_name: inspect._IntrospectableCallable
    ) -> Self:
        """Set object name"""
        self.object_name = object_name
        return self

    def show_intro(self) -> Self:
        """Show introduction"""
        print(f"Inspecting {self.object_name.__name__}\n")
        return self

    def show_type(self) -> Self:
        """Show type"""
        print(f"Type: {type(self.object_name).__name__}")
        return self

    def show_source_code(self) -> Self:
        """Show source code"""
        print(f"Source Code:\n{inspect.getsource(self.object_name)}")
        return self

    def show_signature(self) -> Self:
        """Show signature"""
        print(f"Signature: {inspect.signature(self.object_name)}")
        return self

    def show_doc_strings(self) -> Self:
        """Show doc string info"""
        print(f"DocString Info: {inspect.getdoc(self.object_name) or 'N/A'}")
        return self


def main():
    """Main function to execute the object inspection."""
    inspect_object(ObjectInspector)


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260120
