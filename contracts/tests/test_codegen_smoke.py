from pathlib import Path
import subprocess

ROOT = Path(__file__).parents[1]


def test_codegen_script_generates_temporary_multilanguage_artifacts() -> None:
    result = subprocess.run(
        ["node", "scripts/generate-contracts.mjs"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=900,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert list((ROOT / "generated/kotlin").rglob("*.kt"))
    expected_python_modules = {
        "cancel_job", "component_failed", "job_cancelled", "job_completed", "job_failed",
    }
    actual_python_modules = {
        path.name for path in (ROOT / "generated/python").iterdir() if path.is_dir()
    }
    assert expected_python_modules <= actual_python_modules
    assert list((ROOT / "generated/dotnet").glob("*.cs"))
    assert (ROOT / "generated/codegen-manifest.json").exists()
    assert not [
        path for path in (ROOT.parent / "apps").rglob("generated")
        if "build" not in path.parts
    ]

    kotlin_models = {
        path.stem
        for path in (ROOT / "generated/kotlin/src/main/kotlin").rglob("*.kt")
    }
    assert kotlin_models == {"CursorPage", "ProblemDetails"}


def test_codegen_configuration_documents_provenance() -> None:
    manifest = (ROOT / "manifest.yaml").read_text(encoding="utf-8")
    assert "checksumAlgorithm: sha256" in manifest
    assert "openapi-generator@7.12.0" in manifest
    assert "datamodel-code-generator@0.76.2" in manifest
    assert "NJsonSchema.CodeGeneration.CSharp@11.3.2" in manifest
