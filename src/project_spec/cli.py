from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from .compiler import compile_project
from .report import build_portfolio_report
from .validator import validate_portfolio, validate_project


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="specctl")
    sub = root.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("bundle")
    compile_cmd.add_argument("project_dir", type=Path)
    compile_cmd.add_argument("--output", type=Path)
    validate = sub.add_parser("validate")
    validate.add_argument("path", type=Path)
    validate.add_argument("--project", action="store_true")
    validate.add_argument("--repo-root", type=Path)
    report = sub.add_parser("report")
    report.add_argument("portfolio_root", type=Path)
    report.add_argument("--output", type=Path, required=True)
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "bundle":
            compile_project(args.project_dir, args.output)
            print(args.output or args.project_dir / "project.bundle.yaml")
            return 0
        if args.command == "validate":
            issues = validate_project(args.path, args.repo_root) if args.project else validate_portfolio(args.path)
            print(json.dumps([i.__dict__ for i in issues], indent=2, sort_keys=True))
            return 1 if any(i.severity == "error" for i in issues) else 0
        if args.command == "report":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(build_portfolio_report(args.portfolio_root), encoding="utf-8")
            print(args.output)
            return 0
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
