from __future__ import annotations

import ast
from pathlib import Path

SOURCE_ROOT = Path(__file__).parents[2] / "src" / "indexshelf_data"
LAYER_ORDER = ("domain", "application", "adapters", "apps")
PROVIDER_MODULES = ("scrapling", "crawl4ai", "browser_use", "selenium", "playwright")
DATABASE_MODULES = ("sqlalchemy", "asyncpg", "psycopg", "sqlite3", "databases")
DATABASE_MARKERS = ("PRODUCT_DB", "PRODUCT_DATABASE_URL")


def source_files() -> tuple[Path, ...]:
    return tuple(sorted(SOURCE_ROOT.rglob("*.py")))


def parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def imported_modules(tree: ast.AST) -> tuple[str, ...]:
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None:
            modules.append(node.module)
    return tuple(modules)


def qualified_imported_modules(path: Path) -> tuple[str, ...]:
    tree = parse(path)
    try:
        package = list(path.relative_to(SOURCE_ROOT).with_suffix("").parts)
        package.pop()
    except ValueError:
        package = []
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module is not None:
                modules.append(node.module)
            elif node.level > 0:
                base = package[: len(package) - node.level + 1]
                if node.module:
                    base.append(node.module)
                modules.append("indexshelf_data." + ".".join(base))
    return tuple(modules)


def layer_dependencies(path: Path) -> set[str]:
    parts = path.relative_to(SOURCE_ROOT).parts
    if not parts or parts[0] not in LAYER_ORDER:
        return set()
    return layer_dependencies_for_modules(parts[0], qualified_imported_modules(path))


def layer_dependencies_for_modules(layer: str, modules: tuple[str, ...]) -> set[str]:
    current = LAYER_ORDER.index(layer)
    allowed = set(LAYER_ORDER[: current + 1])
    imported = set()
    for module in modules:
        if module.startswith("indexshelf_data."):
            imported_layer = module.split(".")[1]
            if imported_layer in LAYER_ORDER and imported_layer not in allowed:
                imported.add(imported_layer)
    return imported


def provider_imports(path: Path) -> set[str]:
    return {
        module
        for module in qualified_imported_modules(path)
        if module.split(".")[0] in PROVIDER_MODULES
    }


def database_violations(path: Path) -> set[str]:
    source = path.read_text(encoding="utf-8")
    try:
        layer = path.relative_to(SOURCE_ROOT).parts[0]
    except ValueError:
        layer = ""
    violations = {
        module
        for module in qualified_imported_modules(path)
        if module.split(".")[0] in DATABASE_MODULES and layer in {"domain", "application"}
    }
    violations.update(marker for marker in DATABASE_MARKERS if marker in source)
    return violations


def has_pipeline_branch(source: str) -> bool:
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.Match)):
            branch = (
                node.body
                if isinstance(node, ast.If)
                else [statement for case in node.cases for statement in case.body]
            )
            calls = {
                call.func.id
                for call in ast.walk(ast.Module(body=branch, type_ignores=[]))
                if isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
            }
            if calls.intersection({"route_to_pipeline", "select_pipeline", "run_pipeline"}):
                return True
    return False
