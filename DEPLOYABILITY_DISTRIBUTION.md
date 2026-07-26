# Deployability and distribution

## Deployment unit

A stateless `specctl` CLI for local use, pre-commit checks, and CI.

## Distribution channel

- Python wheel for engineering teams maintaining project specifications.
- Container for CI without host Python configuration.
- Generated Markdown portfolio report for reviewers.

## Activation event

A portfolio activates when registry, segmented specifications, schema metadata, and compiled bundles pass one reproducible command.

## Release invariant

The compiler must never report success when segmented sources and `project.bundle.yaml` differ.
