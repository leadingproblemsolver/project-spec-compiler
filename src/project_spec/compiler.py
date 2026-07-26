from __future__ import annotations

from pathlib import Path
from typing import Any
from .contracts import MANDATORY_SECTIONS, SEGMENT_FILES
from .io import load_yaml, write_yaml


def assemble_project(project_dir: Path) -> dict[str, Any]:
    missing = [filename for filename in SEGMENT_FILES.values() if not (project_dir / filename).is_file()]
    if missing:
        raise ValueError(f"Missing segment files: {', '.join(missing)}")
    bundle: dict[str, Any] = {}
    canonical_schema: dict[str, Any] | None = None
    for section in MANDATORY_SECTIONS:
        path = project_dir / SEGMENT_FILES[section]
        document = load_yaml(path)
        schema = document.get("schema")
        if not isinstance(schema, dict):
            raise ValueError(f"{path} is missing schema metadata")
        if canonical_schema is None:
            canonical_schema = schema
            bundle["schema"] = schema
        elif schema != canonical_schema:
            raise ValueError(f"Schema metadata mismatch in {path}")
        if set(document) != {"schema", section}:
            raise ValueError(f"{path} must contain only schema and {section}")
        bundle[section] = document[section]
    return bundle


def compile_project(project_dir: Path, output: Path | None = None) -> dict[str, Any]:
    bundle = assemble_project(project_dir)
    destination = output or project_dir / "project.bundle.yaml"
    write_yaml(bundle, destination)
    return bundle
