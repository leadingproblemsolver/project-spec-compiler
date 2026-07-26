from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable
from .compiler import assemble_project
from .contracts import ALLOWED_STATUSES, MANDATORY_SECTIONS, SEGMENT_FILES
from .io import load_yaml

@dataclass(frozen=True)
class Issue:
    path: str
    message: str
    severity: str = "error"


def _walk(value: Any, path: str = "") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk(child, f"{path}[{index}]")


def validate_project(project_dir: Path, repo_root: Path | None = None) -> list[Issue]:
    issues: list[Issue] = []
    try:
        compiled = assemble_project(project_dir)
    except (OSError, ValueError) as exc:
        return [Issue(str(project_dir), str(exc))]

    existing_bundle_path = project_dir / "project.bundle.yaml"
    if not existing_bundle_path.is_file():
        issues.append(Issue(str(existing_bundle_path), "Canonical bundle is missing"))
    else:
        try:
            existing = load_yaml(existing_bundle_path)
            if existing != compiled:
                issues.append(Issue(str(existing_bundle_path), "Bundle does not exactly match the segmented source files"))
        except ValueError as exc:
            issues.append(Issue(str(existing_bundle_path), str(exc)))

    schema = compiled.get("schema", {})
    vocabulary = schema.get("status_vocabulary")
    if set(vocabulary or []) != ALLOWED_STATUSES:
        issues.append(Issue("schema.status_vocabulary", "Status vocabulary must match the canonical five values"))

    identity = compiled.get("project_identity", {})
    project_id = identity.get("id")
    repository = identity.get("repository")
    if not isinstance(project_id, str) or not project_id.strip():
        issues.append(Issue("project_identity.id", "Project id is required"))
    if repository != project_dir.name:
        issues.append(Issue("project_identity.repository", f"Expected repository name {project_dir.name!r}"))

    for path, value in _walk(compiled):
        if path.endswith("status") and isinstance(value, str) and value not in ALLOWED_STATUSES:
            issues.append(Issue(path, f"Unknown implementation status: {value}"))

    if repo_root is not None:
        for path, value in _walk(compiled):
            key = path.rsplit(".", 1)[-1]
            if key in {"path", "file", "source", "script"} and isinstance(value, str):
                if value.startswith(("http://", "https://")) or "{{" in value:
                    continue
                candidate = repo_root / value
                if not candidate.exists():
                    issues.append(Issue(path, f"Referenced repository path does not exist: {value}", "warning"))
    return issues


def validate_portfolio(root: Path) -> list[Issue]:
    issues: list[Issue] = []
    registry_path = root / "00_portfolio_registry.yaml"
    contract_path = root / "01_framework_application_contract.yaml"
    for path in (registry_path, contract_path):
        if not path.is_file():
            issues.append(Issue(str(path), "Required portfolio control file is missing"))
    if issues:
        return issues
    try:
        registry = load_yaml(registry_path)
        contract = load_yaml(contract_path)
    except ValueError as exc:
        return [Issue(str(root), str(exc))]

    mandatory = tuple(contract.get("framework_application_contract", {}).get("mandatory_sections", []))
    if mandatory != MANDATORY_SECTIONS:
        issues.append(Issue("framework_application_contract.mandatory_sections", "Mandatory section order or content differs from compiler contract"))

    projects = registry.get("portfolio", {}).get("projects", [])
    seen_ids: set[str] = set()
    seen_repositories: set[str] = set()
    for index, project in enumerate(projects if isinstance(projects, list) else []):
        if not isinstance(project, dict):
            issues.append(Issue(f"portfolio.projects[{index}]", "Project entry must be a mapping"))
            continue
        project_id = project.get("id")
        repository = project.get("repository")
        if project_id in seen_ids:
            issues.append(Issue(f"portfolio.projects[{index}].id", "Duplicate project id"))
        if repository in seen_repositories:
            issues.append(Issue(f"portfolio.projects[{index}].repository", "Duplicate repository"))
        seen_ids.add(project_id)
        seen_repositories.add(repository)
        project_dir = root / str(repository)
        if not project_dir.is_dir():
            issues.append(Issue(f"portfolio.projects[{index}].repository", f"Specification directory is missing: {repository}"))
            continue
        project_issues = validate_project(project_dir)
        issues.extend(Issue(f"{repository}:{i.path}", i.message, i.severity) for i in project_issues)
        try:
            identity = load_yaml(project_dir / SEGMENT_FILES["project_identity"])["project_identity"]
            if identity.get("id") != project_id:
                issues.append(Issue(f"portfolio.projects[{index}].id", "Registry id differs from project identity"))
        except (OSError, ValueError, KeyError) as exc:
            issues.append(Issue(str(project_dir), f"Cannot load project identity: {exc}"))
    return issues
