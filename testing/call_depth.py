#!/usr/bin/env python3
"""Visualize approximate Python function-call depth using the AST.

This performs static analysis. It does not execute the analyzed project.

Examples:
    python call_depth.py src/
    python call_depth.py src/ --root main
    python call_depth.py src/ --root VariableDirector.__post_init__
    python call_depth.py src/ --deepest 20
    python call_depth.py src/ --mermaid call_graph.md
"""

from __future__ import annotations

import argparse
import ast
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Definition:
    """A discovered function or method."""

    qualified_name: str
    module_name: str
    local_name: str
    class_name: str | None
    file_path: Path
    line_number: int

    @property
    def display_location(self) -> str:
        return f"{self.file_path}:{self.line_number}"


@dataclass(slots=True)
class ProjectIndex:
    """Definitions and call relationships discovered in a Python project."""

    definitions: dict[str, Definition] = field(default_factory=dict)
    calls: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )

    by_local_name: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )

    by_class_method: dict[tuple[str, str], set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )

    unresolved_calls: dict[str, set[str]] = field(
        default_factory=lambda: defaultdict(set)
    )


@dataclass(frozen=True, slots=True)
class CallChain:
    """One possible path through the static call graph."""

    nodes: tuple[str, ...]
    cycle_target: str | None = None

    @property
    def depth(self) -> int:
        """Number of call transitions in the chain."""
        return max(0, len(self.nodes) - 1)


class DefinitionCollector(ast.NodeVisitor):
    """Collect module functions and class methods."""

    def __init__(self, file_path: Path, module_name: str) -> None:
        self.file_path = file_path
        self.module_name = module_name
        self.class_stack: list[str] = []
        self.definitions: list[Definition] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record_function(node)
        self.generic_visit(node)

    def _record_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        class_name = ".".join(self.class_stack) or None

        if class_name:
            local_name = f"{class_name}.{node.name}"
        else:
            local_name = node.name

        qualified_name = f"{self.module_name}.{local_name}"

        self.definitions.append(
            Definition(
                qualified_name=qualified_name,
                module_name=self.module_name,
                local_name=local_name,
                class_name=class_name,
                file_path=self.file_path,
                line_number=node.lineno,
            )
        )


class CallCollector(ast.NodeVisitor):
    """Collect calls made inside one function without entering nested functions."""

    def __init__(self) -> None:
        self.calls: set[str] = set()

    def visit_Call(self, node: ast.Call) -> None:
        call_name = render_callable_name(node.func)

        if call_name:
            self.calls.add(call_name)

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        # A nested function has its own call scope.
        return

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        return

    def visit_Lambda(self, node: ast.Lambda) -> None:
        return


class FunctionBodyCollector(ast.NodeVisitor):
    """Associate each function definition with its calls."""

    def __init__(
        self,
        file_path: Path,
        module_name: str,
    ) -> None:
        self.file_path = file_path
        self.module_name = module_name
        self.class_stack: list[str] = []
        self.function_stack: list[str] = []
        self.calls: dict[str, set[str]] = defaultdict(set)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_stack.append(node.name)
        self.generic_visit(node)
        self.class_stack.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._collect_function(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._collect_function(node)

    def _collect_function(
        self,
        node: ast.FunctionDef | ast.AsyncFunctionDef,
    ) -> None:
        class_name = ".".join(self.class_stack)

        if class_name:
            local_name = f"{class_name}.{node.name}"
        else:
            local_name = node.name

        qualified_name = f"{self.module_name}.{local_name}"

        collector = CallCollector()

        for statement in node.body:
            collector.visit(statement)

        self.calls[qualified_name].update(collector.calls)

        # Continue searching for nested function definitions and classes.
        for statement in node.body:
            if isinstance(
                statement,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                ),
            ):
                self.visit(statement)


def render_callable_name(node: ast.expr) -> str | None:
    """Render a callable expression such as self.run or Registry.fetch."""

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        prefix = render_callable_name(node.value)

        if prefix:
            return f"{prefix}.{node.attr}"

        return node.attr

    if isinstance(node, ast.Call):
        # Handles factory()() approximately.
        return render_callable_name(node.func)

    if isinstance(node, ast.Subscript):
        # Handles registry[name]() approximately as "registry".
        return render_callable_name(node.value)

    return None


def discover_python_files(
    root: Path,
    excluded_directories: set[str],
) -> tuple[Path, ...]:
    """Return Python source files beneath root."""

    if root.is_file():
        if root.suffix != ".py":
            raise ValueError(f"Expected a Python file, received: {root}")

        return (root,)

    files: list[Path] = []

    for file_path in root.rglob("*.py"):
        if any(
            part in excluded_directories
            for part in file_path.relative_to(root).parts
        ):
            continue

        files.append(file_path)

    return tuple(sorted(files))


def module_name_from_path(file_path: Path, root: Path) -> str:
    """Derive a dotted module name from a file path."""

    if root.is_file():
        return file_path.stem

    relative_path = file_path.relative_to(root)
    module_parts = list(relative_path.with_suffix("").parts)

    if module_parts and module_parts[-1] == "__init__":
        module_parts.pop()

    return ".".join(module_parts) or root.name


def parse_file(file_path: Path) -> ast.Module:
    """Parse one Python source file."""

    source = file_path.read_text(encoding="utf-8")

    try:
        return ast.parse(source, filename=str(file_path))
    except SyntaxError as error:
        message = f"Unable to parse {file_path}:{error.lineno}: {error.msg}"
        raise SyntaxError(message) from error


def build_project_index(
    root: Path,
    excluded_directories: set[str],
) -> ProjectIndex:
    """Build definitions and resolved call relationships."""

    index = ProjectIndex()
    syntax_trees: dict[Path, tuple[str, ast.Module]] = {}

    for file_path in discover_python_files(root, excluded_directories):
        module_name = module_name_from_path(file_path, root)
        tree = parse_file(file_path)
        syntax_trees[file_path] = (module_name, tree)

        collector = DefinitionCollector(file_path, module_name)
        collector.visit(tree)

        for definition in collector.definitions:
            index.definitions[definition.qualified_name] = definition
            index.by_local_name[definition.local_name].add(
                definition.qualified_name
            )

            simple_name = definition.local_name.rsplit(".", 1)[-1]
            index.by_local_name[simple_name].add(definition.qualified_name)

            if definition.class_name:
                index.by_class_method[
                    (definition.class_name, simple_name)
                ].add(definition.qualified_name)

    for file_path, (module_name, tree) in syntax_trees.items():
        collector = FunctionBodyCollector(file_path, module_name)
        collector.visit(tree)

        for caller, raw_calls in collector.calls.items():
            caller_definition = index.definitions.get(caller)

            if caller_definition is None:
                continue

            for raw_call in raw_calls:
                resolved = resolve_call(
                    raw_call=raw_call,
                    caller=caller_definition,
                    index=index,
                )

                if resolved:
                    index.calls[caller].update(resolved)
                else:
                    index.unresolved_calls[caller].add(raw_call)

    return index


def resolve_call(
    raw_call: str,
    caller: Definition,
    index: ProjectIndex,
) -> set[str]:
    """Resolve a raw call expression to project definitions."""

    parts = raw_call.split(".")
    called_name = parts[-1]

    # self.method() or cls.method()
    if len(parts) == 2 and parts[0] in {"self", "cls"} and caller.class_name:
        matches = index.by_class_method.get(
            (caller.class_name, called_name),
            set(),
        )

        if matches:
            return set(matches)

    # ClassName.method()
    if len(parts) >= 2:
        possible_class = ".".join(parts[:-1])
        matches = index.by_class_method.get(
            (possible_class, called_name),
            set(),
        )

        if matches:
            return set(matches)

        short_class = parts[-2]
        matches = index.by_class_method.get(
            (short_class, called_name),
            set(),
        )

        if matches:
            return set(matches)

    # Prefer functions in the caller's module.
    same_module = {
        qualified_name
        for qualified_name in index.by_local_name.get(called_name, set())
        if index.definitions[qualified_name].module_name == caller.module_name
    }

    if same_module:
        return same_module

    # Fall back to any project function with that simple name.
    matches = index.by_local_name.get(called_name, set())

    if len(matches) == 1:
        return set(matches)

    return set()


def find_roots(index: ProjectIndex) -> tuple[str, ...]:
    """Find definitions that are never called by another project definition."""

    called = {callee for callees in index.calls.values() for callee in callees}

    roots = set(index.definitions) - called

    return tuple(sorted(roots))


def match_definition(
    query: str,
    index: ProjectIndex,
) -> tuple[str, ...]:
    """Find definitions matching a full name, suffix, or simple name."""

    if query in index.definitions:
        return (query,)

    matches = {
        qualified_name
        for qualified_name in index.definitions
        if qualified_name.endswith(f".{query}")
        or index.definitions[qualified_name].local_name == query
        or index.definitions[qualified_name].local_name.endswith(f".{query}")
    }

    return tuple(sorted(matches))


def collect_call_chains(
    root: str,
    index: ProjectIndex,
    maximum_depth: int,
) -> tuple[CallChain, ...]:
    """Collect leaf and cyclic call chains beginning at root."""

    chains: list[CallChain] = []

    def walk(
        current: str,
        path: tuple[str, ...],
    ) -> None:
        if len(path) - 1 >= maximum_depth:
            chains.append(CallChain(path))
            return

        children = tuple(sorted(index.calls.get(current, set())))

        if not children:
            chains.append(CallChain(path))
            return

        emitted_child = False

        for child in children:
            emitted_child = True

            if child in path:
                chains.append(
                    CallChain(
                        nodes=path + (child,),
                        cycle_target=child,
                    )
                )
                continue

            walk(child, path + (child,))

        if not emitted_child:
            chains.append(CallChain(path))

    walk(root, (root,))

    return tuple(chains)


def maximum_depth_from(
    root: str,
    index: ProjectIndex,
    maximum_depth: int,
) -> int:
    """Calculate the deepest discovered chain beginning at root."""

    chains = collect_call_chains(root, index, maximum_depth)

    return max((chain.depth for chain in chains), default=0)


def shorten_name(
    qualified_name: str,
    index: ProjectIndex,
) -> str:
    definition = index.definitions[qualified_name]
    return f"{definition.local_name} [{definition.module_name}]"


def print_tree(
    root: str,
    index: ProjectIndex,
    maximum_depth: int,
) -> None:
    """Print one call tree to the terminal."""

    def walk(
        current: str,
        prefix: str,
        path: tuple[str, ...],
        is_last: bool,
    ) -> None:
        connector = "└── " if is_last else "├── "
        definition = index.definitions[current]
        label = shorten_name(current, index)

        if path:
            print(
                f"{prefix}{connector}{label} ({definition.display_location})"
            )
        else:
            print(f"{label} ({definition.display_location})")

        depth = len(path)

        if depth >= maximum_depth:
            next_prefix = prefix + ("    " if is_last else "│   ")
            print(f"{next_prefix}└── … depth limit reached")
            return

        children = tuple(sorted(index.calls.get(current, set())))

        next_prefix = prefix + ("    " if is_last else "│   ") if path else ""

        for position, child in enumerate(children):
            child_is_last = position == len(children) - 1

            if child in path or child == current:
                connector = "└── " if child_is_last else "├── "
                print(
                    f"{next_prefix}{connector}"
                    f"{shorten_name(child, index)} ↻ cycle"
                )
                continue

            walk(
                current=child,
                prefix=next_prefix,
                path=path + (current,),
                is_last=child_is_last,
            )

    walk(
        current=root,
        prefix="",
        path=(),
        is_last=True,
    )


def write_mermaid(
    output_path: Path,
    selected_roots: Iterable[str],
    index: ProjectIndex,
    maximum_depth: int,
) -> None:
    """Write a Mermaid flowchart for the selected roots."""

    discovered_nodes: set[str] = set()
    discovered_edges: set[tuple[str, str]] = set()
    cycle_edges: set[tuple[str, str]] = set()

    def walk(
        current: str,
        path: tuple[str, ...],
    ) -> None:
        discovered_nodes.add(current)

        if len(path) >= maximum_depth:
            return

        for child in index.calls.get(current, set()):
            discovered_nodes.add(child)
            discovered_edges.add((current, child))

            if child in path or child == current:
                cycle_edges.add((current, child))
                continue

            walk(child, path + (current,))

    for root in selected_roots:
        walk(root, ())

    node_ids = {
        name: f"node_{position}"
        for position, name in enumerate(sorted(discovered_nodes))
    }

    lines = [
        "# Static Python call graph",
        "",
        "```mermaid",
        "flowchart TD",
    ]

    for name in sorted(discovered_nodes):
        definition = index.definitions[name]
        label = (
            f"{definition.local_name}"
            f"<br/>{definition.module_name}"
            f"<br/>line {definition.line_number}"
        )
        safe_label = label.replace('"', "'")
        lines.append(f'    {node_ids[name]}["{safe_label}"]')

    for caller, callee in sorted(discovered_edges):
        arrow = "-. cycle .->" if (caller, callee) in cycle_edges else "-->"
        lines.append(f"    {node_ids[caller]} {arrow} {node_ids[callee]}")

    lines.extend(["```", ""])

    output_path.write_text("\n".join(lines), encoding="utf-8")


def print_deepest_definitions(
    index: ProjectIndex,
    count: int,
    maximum_depth: int,
) -> None:
    """Print definitions ranked by their deepest call chain."""

    rankings = sorted(
        (
            (
                maximum_depth_from(
                    root=qualified_name,
                    index=index,
                    maximum_depth=maximum_depth,
                ),
                qualified_name,
            )
            for qualified_name in index.definitions
        ),
        key=lambda item: (-item[0], item[1]),
    )

    print("Deepest static call chains")
    print("=" * 72)

    for depth, qualified_name in rankings[:count]:
        definition = index.definitions[qualified_name]
        print(
            f"{depth:>3}  {definition.local_name:<40} {definition.module_name}"
        )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visualize approximate Python function-call depth."
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Python file or project source directory.",
    )
    parser.add_argument(
        "--root",
        action="append",
        default=[],
        help=(
            "Function or method to use as a call-tree root. "
            "May be supplied more than once."
        ),
    )
    parser.add_argument(
        "--deepest",
        type=int,
        metavar="COUNT",
        help="Rank this many functions by maximum call depth.",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=20,
        help="Maximum traversal depth. Default: 20.",
    )
    parser.add_argument(
        "--mermaid",
        type=Path,
        help="Write the selected call graph to a Mermaid Markdown file.",
    )
    parser.add_argument(
        "--show-unresolved",
        action="store_true",
        help="Show calls that could not be mapped to project definitions.",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="Additional directory name to exclude.",
    )

    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    root_path = arguments.path.expanduser().resolve()

    if not root_path.exists():
        raise FileNotFoundError(f"Path does not exist: {root_path}")

    excluded_directories = {
        ".git",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".tox",
        ".venv",
        "__pycache__",
        "build",
        "dist",
        "site-packages",
        *arguments.exclude,
    }

    index = build_project_index(
        root=root_path,
        excluded_directories=excluded_directories,
    )

    if not index.definitions:
        print("No Python function or method definitions were discovered.")
        return 1

    print(
        f"Discovered {len(index.definitions)} definitions and "
        f"{sum(len(calls) for calls in index.calls.values())} "
        "resolved call relationships."
    )
    print()

    if arguments.deepest:
        print_deepest_definitions(
            index=index,
            count=arguments.deepest,
            maximum_depth=arguments.max_depth,
        )
        print()

    selected_roots: list[str] = []

    if arguments.root:
        for root_query in arguments.root:
            matches = match_definition(root_query, index)

            if not matches:
                print(f"No definition matched: {root_query}")
                continue

            if len(matches) > 1:
                print(f"Multiple definitions matched {root_query!r}:")

                for match in matches:
                    print(f"  {match}")

                print("Use a more qualified name to select one.")
                continue

            selected_roots.append(matches[0])
    elif not arguments.deepest:
        selected_roots.extend(find_roots(index))

    for position, selected_root in enumerate(selected_roots):
        if position:
            print()

        depth = maximum_depth_from(
            root=selected_root,
            index=index,
            maximum_depth=arguments.max_depth,
        )

        print(f"Root: {selected_root}")
        print(f"Maximum discovered depth: {depth}")
        print_tree(
            root=selected_root,
            index=index,
            maximum_depth=arguments.max_depth,
        )

    if arguments.mermaid:
        if not selected_roots:
            raise ValueError("--mermaid requires at least one selected root.")

        write_mermaid(
            output_path=arguments.mermaid,
            selected_roots=selected_roots,
            index=index,
            maximum_depth=arguments.max_depth,
        )

        print()
        print(f"Mermaid graph written to {arguments.mermaid}")

    if arguments.show_unresolved:
        print()
        print("Unresolved external or dynamic calls")
        print("=" * 72)

        for caller in sorted(index.unresolved_calls):
            unresolved = sorted(index.unresolved_calls[caller])

            if not unresolved:
                continue

            print(shorten_name(caller, index))

            for call_name in unresolved:
                print(f"    ? {call_name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
