from importlib import import_module
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))


for module_path in Path("generated/python").rglob("*.py"):
    if module_path.name.startswith("__"):
        continue
    relative = module_path.relative_to(Path("generated/python")).with_suffix("")
    import_module("generated.python." + ".".join(relative.parts))

expected_modules = {"cancel_job", "component_failed", "job_cancelled", "job_completed", "job_failed"}
actual_modules = {path.name for path in Path("generated/python").iterdir() if path.is_dir()}
missing = expected_modules - actual_modules
if missing:
    raise AssertionError(f"Missing generated Python contract modules: {sorted(missing)}")
