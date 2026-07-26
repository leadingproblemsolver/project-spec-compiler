# Project Specification Compiler

Executable controls for the supplied engineering project specifications.

The original specification set was well structured but manually maintained. This repository makes its most important invariants machine-checkable:

- every project contains the eight mandatory sections;
- every segment uses identical schema metadata;
- only the canonical implementation-status vocabulary is accepted;
- the bundle must exactly equal the segmented source files;
- registry IDs and repository directories must agree;
- optional repository-path checks expose documentation drift;
- a deterministic portfolio report can be generated in CI.

## Quick start

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e '.[dev]'
specctl validate specifications
specctl bundle specifications/cgebs-execution-kernel
specctl report specifications --output var/portfolio-report.md
pytest -q
```

## Repository truth check

```bash
specctl validate specifications/cgebs-execution-kernel \
  --project \
  --repo-root ../cgebs-execution-kernel
```

Path checks are warnings because specification fields sometimes contain examples or future-state locations. Section, schema, bundle, and registry failures are hard errors.

## Deployment

The compiler is a stateless CLI suitable for local pre-commit use or CI. See `docs/deployment.md` and `infra/Dockerfile`.
