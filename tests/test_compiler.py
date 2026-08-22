from pathlib import Path
import shutil
from project_spec._vendor import yaml
from project_spec.compiler import compile_project
from project_spec.validator import validate_portfolio, validate_project

ROOT = Path(__file__).parents[1] / "specifications"

def test_portfolio_passes():
    assert not [i for i in validate_portfolio(ROOT) if i.severity == "error"]

def test_each_project_has_eight_sections(tmp_path):
    for name in ("cgebs-execution-kernel", "signalops-workbench"):
        bundle = compile_project(ROOT / name, tmp_path / f"{name}.yaml")
        assert len(bundle) == 9

def test_bundle_matches_segments():
    for name in ("cgebs-execution-kernel", "signalops-workbench"):
        assert not [i for i in validate_project(ROOT / name) if i.severity == "error"]

def test_schema_mismatch_is_rejected(tmp_path):
    project = tmp_path / "cgebs-execution-kernel"
    shutil.copytree(ROOT / "cgebs-execution-kernel", project)
    path = project / "02_system_architecture.yaml"
    data = yaml.safe_load(path.read_text())
    data["schema"]["version"] = "999"
    path.write_text(yaml.safe_dump(data, sort_keys=False))
    issues = validate_project(project)
    assert any("Schema metadata mismatch" in issue.message for issue in issues)

def test_missing_segment_is_rejected(tmp_path):
    project = tmp_path / "signalops-workbench"
    shutil.copytree(ROOT / "signalops-workbench", project)
    (project / "03_state_contracts_and_invariants.yaml").unlink()
    issues = validate_project(project)
    assert any("Missing segment files" in issue.message for issue in issues)

def test_stale_bundle_is_rejected(tmp_path):
    project = tmp_path / "signalops-workbench"
    shutil.copytree(ROOT / "signalops-workbench", project)
    bundle = yaml.safe_load((project / "project.bundle.yaml").read_text())
    bundle["project_identity"]["name"] = "stale"
    (project / "project.bundle.yaml").write_text(yaml.safe_dump(bundle, sort_keys=False))
    issues = validate_project(project)
    assert any("does not exactly match" in issue.message for issue in issues)

def test_registry_identity_mismatch_is_rejected(tmp_path):
    portfolio = tmp_path / "specifications"
    shutil.copytree(ROOT, portfolio)
    registry = yaml.safe_load((portfolio / "00_portfolio_registry.yaml").read_text())
    registry["portfolio"]["projects"][0]["id"] = "wrong"
    (portfolio / "00_portfolio_registry.yaml").write_text(yaml.safe_dump(registry, sort_keys=False))
    issues = validate_portfolio(portfolio)
    assert any("Registry id differs" in issue.message for issue in issues)
