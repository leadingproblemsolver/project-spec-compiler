from __future__ import annotations

from pathlib import Path
from typing import Any
from ._vendor import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"Top-level YAML in {path} must be a mapping")
    return value


def write_yaml(value: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(value, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8")
