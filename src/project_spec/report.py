from __future__ import annotations

from pathlib import Path
from typing import Any
from .io import load_yaml
from .validator import validate_portfolio


def build_portfolio_report(root: Path) -> str:
    registry = load_yaml(root / "00_portfolio_registry.yaml")
    projects = registry.get("portfolio", {}).get("projects", [])
    issues = validate_portfolio(root)
    lines = ["# Project Specification Portfolio Report", "", f"Projects: **{len(projects)}**", ""]
    for project in projects:
        lines.extend([
            f"## {project.get('repository')}",
            f"- ID: `{project.get('id')}`",
            f"- Role: `{project.get('role')}`",
            f"- Maturity: `{project.get('current_maturity')}`",
            f"- Primary output: {project.get('primary_output')}",
            "",
        ])
    errors = [i for i in issues if i.severity == "error"]
    warnings = [i for i in issues if i.severity != "error"]
    lines.extend(["## Validation", f"- Errors: **{len(errors)}**", f"- Warnings: **{len(warnings)}**", ""])
    for issue in issues:
        lines.append(f"- **{issue.severity.upper()}** `{issue.path}` — {issue.message}")
    if not issues:
        lines.append("All registry, segment, schema, and bundle checks passed.")
    return "\n".join(lines) + "\n"
